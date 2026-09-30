import asyncio
import base64
import json
import os
import subprocess
import time
import urllib.request
import websockets

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE_DIR = r"D:\phan-loai-van-ban-naive-bayes\.chrome_profile"
TARGET_URL = "https://phan-loai-van-ban-naive-bayes.streamlit.app/"
EVIDENCE_DIR = r"D:\phan-loai-van-ban-naive-bayes\docs\evidence\plan-10"

os.makedirs(EVIDENCE_DIR, exist_ok=True)



class StreamlitLiveAuditorPlan10:
    def __init__(self):
        self.proc = None
        self.ws = None
        self.req_id = 0

    def start_browser(self):
        cmd = [
            CHROME_PATH,
            "--headless=new",
            "--remote-debugging-port=9222",
            f"--user-data-dir={PROFILE_DIR}",
            "--window-size=1280,1024",
            TARGET_URL,
        ]
        self.proc = subprocess.Popen(cmd)
        time.sleep(6)

    def stop_browser(self):
        if self.proc:
            self.proc.terminate()
            self.proc = None

    async def connect(self):
        with urllib.request.urlopen("http://127.0.0.1:9222/json/list") as r:
            pages = json.loads(r.read().decode("utf-8"))
            page_target = [p for p in pages if p.get("type") == "page"][0]
            ws_url = page_target["webSocketDebuggerUrl"]
        self.ws = await websockets.connect(ws_url, max_size=50 * 1024 * 1024)
        try:
            await self.cdp("Page.setDownloadBehavior", {
                "behavior": "allow",
                "downloadPath": EVIDENCE_DIR,
            })
            print("  [Page.setDownloadBehavior enabled]")
        except Exception as e:
            print("  [Page.setDownloadBehavior error]:", e)

    async def cdp(self, method, params=None):
        self.req_id += 1
        msg = {"id": self.req_id, "method": method, "params": params or {}}
        await self.ws.send(json.dumps(msg))
        while True:
            raw = await self.ws.recv()
            data = json.loads(raw)
            if data.get("id") == self.req_id:
                return data.get("result", {})

    async def eval_js(self, expr):
        res = await self.cdp("Runtime.evaluate", {
            "expression": expr,
            "returnByValue": True,
            "awaitPromise": True,
        })
        if "exceptionDetails" in res:
            exc = res["exceptionDetails"].get("exception", {}).get("description") or res["exceptionDetails"]
            print("  [JS Exception]:", exc)
        return res.get("result", {}).get("value")

    async def screenshot(self, filename):
        res = await self.cdp("Page.captureScreenshot", {"format": "png"})
        data = res.get("data")
        if data:
            path = os.path.join(EVIDENCE_DIR, filename)
            with open(path, "wb") as f:
                f.write(base64.b64decode(data))
            print(f"  [Screenshot saved] {filename}")
            return path
        return None

    async def wait_for_app_ready(self, timeout=40):
        print("Waiting for Streamlit app iframe to load...")
        for i in range(timeout):
            await asyncio.sleep(1)
            ready = await self.eval_js("""
            (() => {
                const iframe = document.querySelector('iframe');
                if (!iframe) return false;
                try {
                    const doc = iframe.contentDocument || iframe.contentWindow.document;
                    return doc.querySelector('textarea') !== null;
                } catch(e) {
                    return false;
                }
            })()
            """)
            if ready:
                print(f"Streamlit app ready after {i+1} seconds!")
                await asyncio.sleep(2)
                return True
        raise TimeoutError("Streamlit app failed to load inside iframe within timeout.")

    async def input_text(self, text):
        js = f"""
        (() => {{
            const iframe = document.querySelector('iframe');
            const doc = iframe.contentDocument || iframe.contentWindow.document;
            const ta = doc.querySelector('textarea');
            if (!ta) return false;
            const valueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
            valueSetter.call(ta, {json.dumps(text)});
            ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
            ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
            ta.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', ctrlKey: true, bubbles: true }}));
            ta.blur();
            return true;
        }})()
        """
        res = await self.eval_js(js)
        await asyncio.sleep(1.0)
        return res


    async def click_classify(self):
        js = """
        (() => {
            const iframe = document.querySelector('iframe');
            const doc = iframe.contentDocument || iframe.contentWindow.document;
            const buttons = Array.from(doc.querySelectorAll('button'));
            const btn = buttons.find(b => (b.innerText || '').includes('Phân loại'));
            if (btn) {
                btn.click();
                return true;
            }
            return false;
        })()
        """
        res = await self.eval_js(js)
        await asyncio.sleep(0.5)
        return res

    async def click_clear_history(self):
        js = """
        (() => {
            const iframe = document.querySelector('iframe');
            const doc = iframe.contentDocument || iframe.contentWindow.document;
            const buttons = Array.from(doc.querySelectorAll('button'));
            const btn = buttons.find(b => (b.innerText || '').includes('Xóa lịch sử'));
            if (btn) {
                btn.click();
                return true;
            }
            return false;
        })()
        """
        res = await self.eval_js(js)
        await asyncio.sleep(0.5)
        return res

    async def wait_for_computation(self, timeout=15):
        for _ in range(timeout * 2):
            await asyncio.sleep(0.5)
            is_running = await self.eval_js("""
            (() => {
                const iframe = document.querySelector('iframe');
                if (!iframe) return false;
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                const status = doc.querySelector('[data-testid="stStatusWidget"]');
                return status !== null;
            })()
            """)
            if not is_running:
                await asyncio.sleep(0.5)
                return True
        return False

    async def extract_state(self):
        js = """
        (() => {
            try {
                const iframe = document.querySelector('iframe');
                const doc = iframe.contentDocument || iframe.contentWindow.document;

                // Alerts (warnings, errors, info)
                const alerts = Array.from(doc.querySelectorAll('[data-testid="stAlert"]')).map(a => (a.innerText || "").trim());

                // Result box
                const resultBox = doc.querySelector('.result-box');
                const uncertaintyBox = doc.querySelector('.uncertainty-box');

                let predClass = null;
                let confidence = null;
                let vnName = null;
                let latency = null;

                if (resultBox) {
                    const text = resultBox.innerText || "";
                    const lines = text.split('\\n').map(l => l.trim()).filter(Boolean);
                    for (const line of lines) {
                        if (line.includes("Chủ đề dự đoán:")) {
                            predClass = line.split("Chủ đề dự đoán:")[1].trim();
                        } else if (line.includes("Tên tiếng Việt:")) {
                            vnName = line.split("Tên tiếng Việt:")[1].trim();
                        } else if (line.includes("Độ tin cậy")) {
                            const match = line.match(/([0-9.]+)%/);
                            if (match) confidence = parseFloat(match[1]);
                        } else if (line.includes("Thời gian xử lý:")) {
                            const part = line.split("Thời gian xử lý:")[1] || "";
                            latency = parseFloat(part.replace("ms", "").trim());
                        }
                    }
                }

                // Explanations table
                const tables = Array.from(doc.querySelectorAll('table')).map(t => {
                    const headers = Array.from(t.querySelectorAll('th')).map(th => (th.innerText || "").trim());
                    const rows = Array.from(t.querySelectorAll('tr')).map(tr =>
                        Array.from(tr.querySelectorAll('td')).map(td => (td.innerText || "").trim())
                    ).filter(r => r.length > 0);
                    return { headers, rows };
                });

                // Isolate HISTORY rows count specifically from caption "Tổng số lượt dự đoán: X"
                let isolatedHistoryCount = 0;
                let hasHistory = false;
                const captions = Array.from(doc.querySelectorAll('[data-testid="stCaptionContainer"], p, small, span'));
                for (const c of captions) {
                    const txt = (c.innerText || '').trim();
                    const m = txt.match(/Tổng số lượt dự đoán:\s*(\d+)/i);
                    if (m) {
                        isolatedHistoryCount = parseInt(m[1], 10);
                        hasHistory = true;
                        break;
                    }
                }
                const emptyNotice = Array.from(doc.querySelectorAll('p, span, div, caption')).some(el => (el.innerText || '').includes('Chưa có lượt dự đoán nào trong phiên hiện tại'));

                // Download CSV button
                const downloadBtn = Array.from(doc.querySelectorAll('a[download], a, button')).find(b => (b.innerText || "").includes('Tải lịch sử'));
                let downloadHref = null;
                let downloadFilename = null;
                if (downloadBtn) {
                    downloadHref = downloadBtn.getAttribute ? downloadBtn.getAttribute('href') : null;
                    downloadFilename = downloadBtn.getAttribute ? downloadBtn.getAttribute('download') : null;
                }

                // Footer version caption
                const footerEl = Array.from(doc.querySelectorAll('p, small, span')).find(el => (el.innerText || '').includes('Phân loại văn bản Naive Bayes') || (el.innerText || '').includes('v1.0.'));
                const footerText = footerEl ? (footerEl.innerText || '').trim() : null;

                return {
                    has_result_box: !!resultBox,
                    pred_class: predClass,
                    confidence: confidence,
                    vn_name: vnName,
                    latency_ms: latency,
                    result_box_text: resultBox ? resultBox.innerText : null,
                    uncertainty_box_text: uncertaintyBox ? uncertaintyBox.innerText : null,
                    alerts: alerts,
                    tables: tables,
                    isolated_history_count: isolatedHistoryCount,
                    has_history: hasHistory,
                    empty_notice: emptyNotice,
                    download_button_found: !!downloadBtn,
                    download_href: downloadHref,
                    download_filename: downloadFilename,
                    footer_text: footerText
                };
            } catch(e) {
                return { error: e.toString(), stack: e.stack };
            }
        })()
        """
        res = await self.eval_js(js)
        if isinstance(res, dict) and "error" in res:
            print("  [extract_state Error]:", res.get("error"))
        return res

    async def fetch_csv_content(self):
        js = """
        (async () => {
            try {
                const iframe = document.querySelector('iframe');
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                const a = doc.querySelector('a[download]') || Array.from(doc.querySelectorAll('a')).find(x => (x.innerText || '').includes('Tải lịch sử') || x.getAttribute('download'));
                if (!a) return null;
                const href = a.getAttribute('href');
                if (!href) return null;
                if (href.startsWith('data:')) {
                    const commaIdx = href.indexOf(',');
                    if (commaIdx >= 0) {
                        return decodeURIComponent(href.slice(commaIdx + 1));
                    }
                }
                const resp = await fetch(href);
                return await resp.text();
            } catch(e) {
                return 'ERROR: ' + e.toString();
            }
        })()
        """
        return await self.eval_js(js)


async def run_audit():
    print("=====================================================================")
    print("STARTING STREAMLIT CLOUD LIVE VERIFICATION & AUDIT (PLAN 10)")
    print(f"Target URL: {TARGET_URL}")
    print(f"Evidence Dir: {EVIDENCE_DIR}")
    print("=====================================================================")

    auditor = StreamlitLiveAuditorPlan10()
    results = {}

    try:
        auditor.start_browser()
        await auditor.connect()
        await auditor.wait_for_app_ready()

        # -------------------------------------------------------------
        # TC 00: Initial Load & Version
        # -------------------------------------------------------------
        print("\n--- Running TC-00: Initial Load & App Version ---")
        s00 = await auditor.extract_state()
        await auditor.screenshot("tc00_initial_load.png")
        results["tc00_initial_load"] = {
            "footer_text": s00.get("footer_text"),
            "empty_notice": s00.get("empty_notice"),
            "screenshot": "tc00_initial_load.png",
            "status": "PASS" if s00.get("empty_notice") else "OBSERVED"
        }
        print(f"  Footer text: {s00.get('footer_text')}")
        print(f"  Empty history notice present: {s00.get('empty_notice')}")

        # -------------------------------------------------------------
        # TC 01: Empty input on fresh session
        # -------------------------------------------------------------
        print("\n--- Running TC-01: Empty Input On Fresh Session ---")
        await auditor.input_text("")
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s01 = await auditor.extract_state()
        await auditor.screenshot("tc01_empty_input.png")
        has_empty_warning = any("Vui lòng nhập nội dung văn bản" in a for a in s01["alerts"])
        results["tc01_empty_input"] = {
            "input": "",
            "has_result_box": s01["has_result_box"],
            "alerts": s01["alerts"],
            "isolated_history_count": s01["isolated_history_count"],
            "empty_notice": s01["empty_notice"],
            "screenshot": "tc01_empty_input.png",
            "status": "PASS" if has_empty_warning and not s01["has_result_box"] and s01["isolated_history_count"] == 0 else "FAIL"
        }
        print(f"  Result box: {s01['has_result_box']} (expected False)")
        print(f"  History count: {s01['isolated_history_count']} (expected 0)")
        print(f"  Alerts: {s01['alerts']}")

        # -------------------------------------------------------------
        # TC 02: Whitespace-only input on fresh session
        # -------------------------------------------------------------
        print("\n--- Running TC-02: Whitespace-Only Input ---")
        await auditor.input_text("     \t\n   ")
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s02 = await auditor.extract_state()
        await auditor.screenshot("tc02_whitespace_input.png")
        has_ws_warning = any("Vui lòng nhập nội dung văn bản" in a for a in s02["alerts"])
        results["tc02_whitespace_input"] = {
            "input": "     \\t\\n   ",
            "has_result_box": s02["has_result_box"],
            "alerts": s02["alerts"],
            "isolated_history_count": s02["isolated_history_count"],
            "screenshot": "tc02_whitespace_input.png",
            "status": "PASS" if has_ws_warning and not s02["has_result_box"] and s02["isolated_history_count"] == 0 else "FAIL"
        }
        print(f"  Result box: {s02['has_result_box']} (expected False)")
        print(f"  History count: {s02['isolated_history_count']} (expected 0)")

        # -------------------------------------------------------------
        # TC 03: 1st valid prediction: Graphics
        # -------------------------------------------------------------
        print("\n--- Running TC-03: 1st Valid (Graphics) ---")
        t03_input = "The graphics software renders three dimensional images using polygons, textures and computer animation."
        await auditor.input_text(t03_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s03 = await auditor.extract_state()
        await auditor.screenshot("tc03_graphics.png")
        results["tc03_graphics"] = {
            "input": t03_input,
            "pred_class": s03["pred_class"],
            "confidence": s03["confidence"],
            "vn_name": s03["vn_name"],
            "latency_ms": s03["latency_ms"],
            "isolated_history_count": s03["isolated_history_count"],
            "screenshot": "tc03_graphics.png",
            "status": "PASS" if s03["pred_class"] == "comp.graphics" and s03["isolated_history_count"] == 1 else "FAIL"
        }
        print(f"  Predicted: {s03['pred_class']} ({s03['confidence']}%), History count: {s03['isolated_history_count']}")

        # -------------------------------------------------------------
        # TC 04: Whitespace input AFTER valid prediction (must NOT increase history)
        # -------------------------------------------------------------
        print("\n--- Running TC-04: Whitespace After Valid (Must NOT Add History) ---")
        await auditor.input_text("    ")
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s04 = await auditor.extract_state()
        await auditor.screenshot("tc04_whitespace_after_valid.png")
        has_warning_04 = any("Vui lòng nhập nội dung văn bản" in a for a in s04["alerts"])
        results["tc04_whitespace_after_valid"] = {
            "input": "    ",
            "alerts": s04["alerts"],
            "isolated_history_count": s04["isolated_history_count"],
            "screenshot": "tc04_whitespace_after_valid.png",
            "status": "PASS" if has_warning_04 and s04["isolated_history_count"] == 1 else "FAIL"
        }
        print(f"  Warning present: {has_warning_04}, History count: {s04['isolated_history_count']} (expected strictly 1)")

        # -------------------------------------------------------------
        # TC 05: 2nd valid prediction: Baseball
        # -------------------------------------------------------------
        print("\n--- Running TC-05: Baseball ---")
        t05_input = "The baseball pitcher threw the ball and the batter hit a home run during the game."
        await auditor.input_text(t05_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s05 = await auditor.extract_state()
        await auditor.screenshot("tc05_baseball.png")
        results["tc05_baseball"] = {
            "input": t05_input,
            "pred_class": s05["pred_class"],
            "confidence": s05["confidence"],
            "isolated_history_count": s05["isolated_history_count"],
            "screenshot": "tc05_baseball.png",
            "status": "PASS" if s05["pred_class"] == "rec.sport.baseball" and s05["isolated_history_count"] == 2 else "FAIL"
        }
        print(f"  Predicted: {s05['pred_class']} ({s05['confidence']}%), History count: {s05['isolated_history_count']}")

        # -------------------------------------------------------------
        # TC 06: 3rd valid prediction: Space (NASA sentence)
        # -------------------------------------------------------------
        print("\n--- Running TC-06: Space (NASA) ---")
        t06_input = "NASA launched a spacecraft into orbit to study distant planets and explore the solar system."
        await auditor.input_text(t06_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s06 = await auditor.extract_state()
        await auditor.screenshot("tc06_space_nasa.png")
        results["tc06_space_nasa"] = {
            "input": t06_input,
            "pred_class": s06["pred_class"],
            "confidence": s06["confidence"],
            "isolated_history_count": s06["isolated_history_count"],
            "screenshot": "tc06_space_nasa.png",
            "status": "PASS" if s06["pred_class"] == "sci.space" and s06["isolated_history_count"] == 3 else "FAIL"
        }
        print(f"  Predicted: {s06['pred_class']} ({s06['confidence']}%), History count: {s06['isolated_history_count']}")

        # -------------------------------------------------------------
        # TC 07: 4th valid prediction: Politics
        # -------------------------------------------------------------
        print("\n--- Running TC-07: Politics ---")
        t07_input = "The government and parliament debated public policy, elections and political reforms."
        await auditor.input_text(t07_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s07 = await auditor.extract_state()
        await auditor.screenshot("tc07_politics.png")
        results["tc07_politics"] = {
            "input": t07_input,
            "pred_class": s07["pred_class"],
            "confidence": s07["confidence"],
            "isolated_history_count": s07["isolated_history_count"],
            "screenshot": "tc07_politics.png",
            "status": "PASS" if s07["pred_class"] == "talk.politics.misc" and s07["isolated_history_count"] == 4 else "FAIL"
        }
        print(f"  Predicted: {s07['pred_class']} ({s07['confidence']}%), History count: {s07['isolated_history_count']}")

        # -------------------------------------------------------------
        # TC 08: Short text 'space' (Fix check: NO '(Rỗng)' suffix!)
        # -------------------------------------------------------------
        print("\n--- Running TC-08: Short Text ('space') ---")
        t08_input = "space"
        await auditor.input_text(t08_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s08 = await auditor.extract_state()
        await auditor.screenshot("tc08_short_space.png")
        results["tc08_short_space"] = {
            "input": t08_input,
            "pred_class": s08["pred_class"],
            "confidence": s08["confidence"],
            "alerts": s08["alerts"],
            "isolated_history_count": s08["isolated_history_count"],
            "screenshot": "tc08_short_space.png",
            "status": "PASS" if s08["isolated_history_count"] == 5 else "FAIL"
        }
        print(f"  Predicted: {s08['pred_class']} ({s08['confidence']}%), Alerts: {s08['alerts']}")

        # -------------------------------------------------------------
        # TC 09: OOV text 'zxqvbnm qqqzxvv' (Fix check: NO '(Rỗng)' suffix!)
        # -------------------------------------------------------------
        print("\n--- Running TC-09: OOV Text ---")
        t09_input = "zxqvbnm qqqzxvv"
        await auditor.input_text(t09_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s09 = await auditor.extract_state()
        await auditor.screenshot("tc09_oov.png")
        has_oov_alert = any("từ điển" in a.lower() or "oov" in a.lower() for a in s09["alerts"])
        results["tc09_oov"] = {
            "input": t09_input,
            "pred_class": s09["pred_class"],
            "confidence": s09["confidence"],
            "alerts": s09["alerts"],
            "isolated_history_count": s09["isolated_history_count"],
            "screenshot": "tc09_oov.png",
            "status": "PASS" if has_oov_alert and s09["isolated_history_count"] == 6 else "FAIL"
        }
        print(f"  OOV Alert: {has_oov_alert}, History count: {s09['isolated_history_count']}")

        # -------------------------------------------------------------
        # TC 10: Low confidence / mixed topics
        # -------------------------------------------------------------
        print("\n--- Running TC-10: Low Confidence ---")
        t10_input = "baseball game software render satellite government debate"
        await auditor.input_text(t10_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s10 = await auditor.extract_state()
        await auditor.screenshot("tc10_low_conf.png")
        results["tc10_low_conf"] = {
            "input": t10_input,
            "pred_class": s10["pred_class"],
            "confidence": s10["confidence"],
            "uncertainty_box": s10["uncertainty_box_text"],
            "isolated_history_count": s10["isolated_history_count"],
            "screenshot": "tc10_low_conf.png",
            "status": "PASS" if s10["isolated_history_count"] == 7 else "FAIL"
        }
        print(f"  Result: {s10['pred_class']} ({s10['confidence']}%), History count: {s10['isolated_history_count']}")

        # -------------------------------------------------------------
        # TC 11: Feature Explanations
        # -------------------------------------------------------------
        print("\n--- Running TC-11: Feature Explanations ---")
        t11_input = "Hubble space telescope orbit astronaut cosmic galaxy exploration"
        await auditor.input_text(t11_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s11 = await auditor.extract_state()
        await auditor.screenshot("tc11_explanations.png")
        results["tc11_explanations"] = {
            "input": t11_input,
            "pred_class": s11["pred_class"],
            "confidence": s11["confidence"],
            "tables_count": len(s11["tables"]),
            "isolated_history_count": s11["isolated_history_count"],
            "screenshot": "tc11_explanations.png",
            "status": "PASS" if len(s11["tables"]) > 0 and s11["isolated_history_count"] == 8 else "FAIL"
        }
        print(f"  Explanations tables found: {len(s11['tables'])}, History count: {s11['isolated_history_count']}")

        # -------------------------------------------------------------
        # TC 12: Exact 80 characters boundary
        # -------------------------------------------------------------
        print("\n--- Running TC-12: Exact 80 Chars Boundary ---")
        t12_input = "The space shuttle orbited the planet Earth and deployed scientific instruments!!"
        assert len(t12_input) == 80
        await auditor.input_text(t12_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s12 = await auditor.extract_state()
        await auditor.screenshot("tc12_boundary_80.png")
        results["tc12_boundary_80"] = {
            "input": t12_input,
            "input_len": len(t12_input),
            "pred_class": s12["pred_class"],
            "isolated_history_count": s12["isolated_history_count"],
            "screenshot": "tc12_boundary_80.png",
            "status": "PASS" if s12["isolated_history_count"] == 9 else "FAIL"
        }
        print(f"  Boundary 80 chars - Predicted: {s12['pred_class']}, History count: {s12['isolated_history_count']}")

        # -------------------------------------------------------------
        # TC 13: Exact 81 characters boundary
        # -------------------------------------------------------------
        print("\n--- Running TC-13: Exact 81 Chars Boundary ---")
        t13_input = t12_input + "X"
        assert len(t13_input) == 81
        await auditor.input_text(t13_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s13 = await auditor.extract_state()
        await auditor.screenshot("tc13_boundary_81.png")
        results["tc13_boundary_81"] = {
            "input": t13_input,
            "input_len": len(t13_input),
            "pred_class": s13["pred_class"],
            "isolated_history_count": s13["isolated_history_count"],
            "screenshot": "tc13_boundary_81.png",
            "status": "PASS" if s13["isolated_history_count"] == 10 else "FAIL"
        }
        print(f"  Boundary 81 chars - Predicted: {s13['pred_class']}, History count: {s13['isolated_history_count']}")

        # -------------------------------------------------------------
        # TC 14: Isolated History Count Check
        # -------------------------------------------------------------
        print("\n--- Running TC-14: History Count Check ---")
        await auditor.screenshot("tc14_history_table.png")
        s14 = await auditor.extract_state()
        results["tc14_history_table"] = {
            "isolated_history_count": s14["isolated_history_count"],
            "screenshot": "tc14_history_table.png",
            "status": "PASS" if s14["isolated_history_count"] == 10 else "FAIL"
        }
        print(f"  Isolated History Count: {s14['isolated_history_count']} (strictly 10)")

        # -------------------------------------------------------------
        # TC 15: Real CSV Download & Deep Content Audit
        # -------------------------------------------------------------
        print("\n--- Running TC-15: Real CSV Download & Deep Audit ---")
        downloaded_name = "lich_su_du_doan_naive_bayes.csv"
        raw_download_path = os.path.join(EVIDENCE_DIR, downloaded_name)
        target_csv_path = os.path.join(EVIDENCE_DIR, "tc15_downloaded_history.csv")
        if os.path.exists(raw_download_path):
            os.remove(raw_download_path)

        click_download_js = """
        (() => {
            const iframe = document.querySelector('iframe');
            const doc = iframe.contentDocument || iframe.contentWindow.document;
            const dlBtn = Array.from(doc.querySelectorAll('a[download], a, button')).find(el => (el.innerText || '').includes('Tải lịch sử'));
            if (dlBtn) {
                dlBtn.click();
                return true;
            }
            return false;
        })()
        """
        clicked_dl = await auditor.eval_js(click_download_js)
        print(f"  Download button clicked via DOM: {clicked_dl}")

        csv_content = None
        for wait_i in range(8):
            await asyncio.sleep(1)
            if os.path.exists(raw_download_path):
                with open(raw_download_path, "r", encoding="utf-8-sig", errors="replace") as f:
                    csv_content = f.read()
                with open(target_csv_path, "w", encoding="utf-8-sig") as f:
                    f.write(csv_content)
                print(f"  Downloaded file intercepted from browser after {wait_i+1}s!")
                break

        if not csv_content:
            csv_content = await auditor.fetch_csv_content()
            if csv_content:
                with open(target_csv_path, "w", encoding="utf-8-sig") as f:
                    f.write(csv_content)

        if csv_content:
            lines = [line.strip() for line in csv_content.strip().splitlines() if line.strip()]
            header = lines[0] if lines else ""
            data_rows = lines[1:]
            row_count = len(data_rows)
            print(f"  Downloaded CSV lines: {len(lines)}, header: {header}")
            print(f"  Data row count: {row_count}")

            # Verify no "(Rỗng)" anywhere in previews of non-empty text
            has_rong_suffix = any("(Rỗng)" in row for row in data_rows)
            has_space_clean = any(",space," in row or row.startswith("space,") or ',"space",' in row for row in data_rows)
            has_oov_clean = any("zxqvbnm qqqzxvv" in row and "zxqvbnm qqqzxvv(Rỗng)" not in row for row in data_rows)

            results["tc15_csv"] = {
                "csv_saved_path": "tc15_downloaded_history.csv",
                "header": header,
                "row_count": row_count,
                "has_rong_suffix": has_rong_suffix,
                "has_space_clean": has_space_clean,
                "has_oov_clean": has_oov_clean,
                "sample_rows": data_rows[:4],
                "status": "PASS" if row_count == 10 and not has_rong_suffix and has_space_clean and has_oov_clean else "FAIL"
            }
            print(f"  Contains '(Rỗng)' suffix: {has_rong_suffix} (expected False)")
            print(f"  Contains clean 'space': {has_space_clean} (expected True)")
            print(f"  Contains clean OOV: {has_oov_clean} (expected True)")
        else:
            results["tc15_csv"] = {"status": "FAIL", "error": "No CSV content captured"}

        # -------------------------------------------------------------
        # TC 16: Clear History
        # -------------------------------------------------------------
        print("\n--- Running TC-16: Clear History ---")
        cleared = await auditor.click_clear_history()
        await asyncio.sleep(2)
        s16 = await auditor.extract_state()
        await auditor.screenshot("tc16_clear_history.png")
        results["tc16_clear_history"] = {
            "cleared_clicked": cleared,
            "isolated_history_count": s16["isolated_history_count"],
            "empty_notice": s16["empty_notice"],
            "screenshot": "tc16_clear_history.png",
            "status": "PASS" if s16["isolated_history_count"] == 0 and s16["empty_notice"] else "FAIL"
        }
        print(f"  History count after clear: {s16['isolated_history_count']}, Empty notice: {s16['empty_notice']}")

        # -------------------------------------------------------------
        # TC 17: Page Reload & Re-predict
        # -------------------------------------------------------------
        print("\n--- Running TC-17: Page Reload & Re-predict ---")
        await auditor.cdp("Page.navigate", {"url": TARGET_URL})
        await auditor.wait_for_app_ready()
        t17_input = "Astronomers observe deep space stellar explosion with radio telescopes."
        await auditor.input_text(t17_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s17 = await auditor.extract_state()
        await auditor.screenshot("tc17_reload.png")
        results["tc17_reload"] = {
            "input": t17_input,
            "pred_class": s17["pred_class"],
            "confidence": s17["confidence"],
            "isolated_history_count": s17["isolated_history_count"],
            "screenshot": "tc17_reload.png",
            "status": "PASS" if s17["pred_class"] == "sci.space" and s17["isolated_history_count"] == 1 else "FAIL"
        }
        print(f"  Reload prediction: {s17['pred_class']} ({s17['confidence']}%), History count: {s17['isolated_history_count']}")

        # Save all structured results
        report_path = os.path.join(EVIDENCE_DIR, "plan10_test_report.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "target_url": TARGET_URL,
                "results": results
            }, f, indent=2, ensure_ascii=False)
        print(f"\nAll tests completed! Report saved to {report_path}")

    finally:
        auditor.stop_browser()


if __name__ == "__main__":
    asyncio.run(run_audit())
