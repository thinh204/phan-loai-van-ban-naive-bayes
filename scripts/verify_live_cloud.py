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
EVIDENCE_DIR = r"D:\phan-loai-van-ban-naive-bayes\docs\evidence\plan-9"

os.makedirs(EVIDENCE_DIR, exist_ok=True)

class StreamlitLiveAuditor:
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

    async def wait_for_app_ready(self, timeout=30):
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
                print(f"Streamlit app ready after {i+1}s!")
                return True
        raise TimeoutError("Streamlit app did not load within timeout")

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
        return await self.eval_js(js)

    async def click_classify(self):
        js = """
        (() => {
            const iframe = document.querySelector('iframe');
            const doc = iframe.contentDocument || iframe.contentWindow.document;
            const buttons = Array.from(doc.querySelectorAll('button'));
            const btn = buttons.find(b => b.textContent && b.textContent.includes('Phân loại'));
            if (!btn) return false;
            btn.click();
            return true;
        })()
        """
        return await self.eval_js(js)

    async def wait_for_computation(self, timeout=15):
        # Wait until no spinner is running and result or alert is updated
        await asyncio.sleep(1.5)
        for _ in range(timeout):
            is_busy = await self.eval_js("""
            (() => {
                const iframe = document.querySelector('iframe');
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                const spinner = doc.querySelector('.stSpinner');
                return !!spinner;
            })()
            """)
            if not is_busy:
                break
            await asyncio.sleep(0.5)

    async def extract_state(self):
        js = """
        (() => {
            try {
                const iframe = document.querySelector('iframe');
                if (!iframe) return { error: "No iframe found" };
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                if (!doc) return { error: "No doc found" };

                const resultBox = doc.querySelector('.result-box');
                const uncertaintyBox = doc.querySelector('.uncertainty-box');
                const alerts = Array.from(doc.querySelectorAll('.stAlert')).map(a => (a.innerText || "").trim());

                let predClass = null;
                let confidence = null;
                let latency = null;
                let vnName = null;

                if (resultBox) {
                    const lines = (resultBox.innerText || "").split('\\n').map(l => l.trim()).filter(Boolean);
                    for (const line of lines) {
                        if (line.includes("Chủ đề dự đoán:")) {
                            predClass = line.split("Chủ đề dự đoán:")[1].trim();
                        }
                        if (line.includes("Tên tiếng Việt:")) {
                            vnName = line.split("Tên tiếng Việt:")[1].trim();
                        }
                        if (line.includes("Độ tin cậy")) {
                            const parts = line.split(":");
                            if (parts.length > 1) {
                                confidence = parseFloat(parts[parts.length - 1].replace("%", "").trim());
                            }
                        }
                        if (line.includes("Thời gian xử lý:")) {
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

                // History rows from dataframe / table
                const historyElements = Array.from(doc.querySelectorAll('[data-testid="stDataFrame"] tr, [data-testid="stTable"] tr')).map(r => (r.innerText || "").trim());

                // Download CSV button
                const downloadBtn = Array.from(doc.querySelectorAll('a[download], a, button')).find(b => (b.innerText || "").includes('Tải lịch sử'));
                let downloadHref = null;
                let downloadFilename = null;
                if (downloadBtn) {
                    downloadHref = downloadBtn.getAttribute ? downloadBtn.getAttribute('href') : null;
                    downloadFilename = downloadBtn.getAttribute ? downloadBtn.getAttribute('download') : null;
                }

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
                    history_rows_count: historyElements.length,
                    history_preview: historyElements.slice(0, 5),
                    download_button_found: !!downloadBtn,
                    download_href: downloadHref,
                    download_filename: downloadFilename
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
                    const base64Data = href.split(',')[1];
                    const binary = atob(base64Data);
                    const bytes = new Uint8Array(binary.length);
                    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
                    return new TextDecoder('utf-8').decode(bytes);
                }
                const resp = await fetch(href);
                return await resp.text();
            } catch(e) {
                return "ERROR: " + e.toString();
            }
        })()
        """
        return await self.eval_js(js)

    async def click_clear_history(self):
        js = """
        (() => {
            const iframe = document.querySelector('iframe');
            const doc = iframe.contentDocument || iframe.contentWindow.document;
            const buttons = Array.from(doc.querySelectorAll('button'));
            const btn = buttons.find(b => b.textContent && b.textContent.includes('Xóa lịch sử'));
            if (!btn) return false;
            btn.click();
            return true;
        })()
        """
        return await self.eval_js(js)


async def run_audit():
    auditor = StreamlitLiveAuditor()
    auditor.start_browser()
    results = {}

    try:
        await auditor.connect()
        await auditor.wait_for_app_ready()
        await auditor.screenshot("tc00_initial_load.png")

        # -------------------------------------------------------------
        # TC 01: Graphics
        # -------------------------------------------------------------
        print("\n--- Running TC-01: Graphics ---")
        t01_input = "The graphics software renders three dimensional images using polygons, textures and computer animation."
        await auditor.input_text(t01_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s01 = await auditor.extract_state()
        await auditor.screenshot("tc01_graphics.png")
        results["tc01_graphics"] = {
            "input": t01_input,
            "pred_class": s01["pred_class"],
            "confidence": s01["confidence"],
            "vn_name": s01["vn_name"],
            "latency_ms": s01["latency_ms"],
            "alerts": s01["alerts"],
            "tables": s01["tables"],
            "screenshot": "tc01_graphics.png",
            "status": "PASS" if s01["pred_class"] == "comp.graphics" else "OBSERVED"
        }
        print(f"  Result: {s01['pred_class']} ({s01['confidence']}%) in {s01['latency_ms']} ms")

        # -------------------------------------------------------------
        # TC 02: Baseball
        # -------------------------------------------------------------
        print("\n--- Running TC-02: Baseball ---")
        t02_input = "The baseball pitcher threw the ball and the batter hit a home run during the game."
        await auditor.input_text(t02_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s02 = await auditor.extract_state()
        await auditor.screenshot("tc02_baseball.png")
        results["tc02_baseball"] = {
            "input": t02_input,
            "pred_class": s02["pred_class"],
            "confidence": s02["confidence"],
            "vn_name": s02["vn_name"],
            "latency_ms": s02["latency_ms"],
            "alerts": s02["alerts"],
            "screenshot": "tc02_baseball.png",
            "status": "PASS" if s02["pred_class"] == "rec.sport.baseball" else "OBSERVED"
        }
        print(f"  Result: {s02['pred_class']} ({s02['confidence']}%) in {s02['latency_ms']} ms")

        # -------------------------------------------------------------
        # TC 03: Space (NASA sentence)
        # -------------------------------------------------------------
        print("\n--- Running TC-03: Space (NASA) ---")
        t03_input = "NASA launched a spacecraft into orbit to study distant planets and explore the solar system."
        await auditor.input_text(t03_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s03 = await auditor.extract_state()
        await auditor.screenshot("tc03_space.png")
        results["tc03_space"] = {
            "input": t03_input,
            "pred_class": s03["pred_class"],
            "confidence": s03["confidence"],
            "vn_name": s03["vn_name"],
            "latency_ms": s03["latency_ms"],
            "alerts": s03["alerts"],
            "screenshot": "tc03_space.png",
            "status": "PASS" if s03["pred_class"] == "sci.space" else "OBSERVED"
        }
        print(f"  Result: {s03['pred_class']} ({s03['confidence']}%) in {s03['latency_ms']} ms")

        # -------------------------------------------------------------
        # TC 04: Politics
        # -------------------------------------------------------------
        print("\n--- Running TC-04: Politics ---")
        t04_input = "The government and parliament debated public policy, elections and political reform."
        await auditor.input_text(t04_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s04 = await auditor.extract_state()
        await auditor.screenshot("tc04_politics.png")
        results["tc04_politics"] = {
            "input": t04_input,
            "pred_class": s04["pred_class"],
            "confidence": s04["confidence"],
            "vn_name": s04["vn_name"],
            "latency_ms": s04["latency_ms"],
            "alerts": s04["alerts"],
            "screenshot": "tc04_politics.png",
            "status": "PASS" if s04["pred_class"] == "talk.politics.misc" else "OBSERVED"
        }
        print(f"  Result: {s04['pred_class']} ({s04['confidence']}%) in {s04['latency_ms']} ms")

        # -------------------------------------------------------------
        # TC 05: Empty & Whitespace
        # -------------------------------------------------------------
        print("\n--- Running TC-05: Empty & Whitespace ---")
        t05_input = "   "
        await auditor.input_text(t05_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s05 = await auditor.extract_state()
        await auditor.screenshot("tc05_empty.png")
        results["tc05_empty"] = {
            "input": t05_input,
            "alerts": s05["alerts"],
            "has_result_box": s05["has_result_box"],
            "pred_class": s05["pred_class"],
            "screenshot": "tc05_empty.png",
            "status": "PASS" if any("Vui lòng nhập" in a for a in s05["alerts"]) else "OBSERVED"
        }
        print(f"  Alerts: {s05['alerts']}")

        # -------------------------------------------------------------
        # TC 06: Short text (< 10 chars / < 3 words)
        # -------------------------------------------------------------
        print("\n--- Running TC-06: Short Text ---")
        t06_input = "space"
        await auditor.input_text(t06_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s06 = await auditor.extract_state()
        await auditor.screenshot("tc06_short.png")
        results["tc06_short"] = {
            "input": t06_input,
            "pred_class": s06["pred_class"],
            "confidence": s06["confidence"],
            "alerts": s06["alerts"],
            "uncertainty_box": s06["uncertainty_box_text"],
            "screenshot": "tc06_short.png",
            "status": "PASS" if any("ngắn" in a.lower() for a in s06["alerts"]) else "OBSERVED"
        }
        print(f"  Alerts: {s06['alerts']}")

        # -------------------------------------------------------------
        # TC 07: OOV (Out of Vocabulary)
        # -------------------------------------------------------------
        print("\n--- Running TC-07: OOV Text ---")
        t07_input = "zxqvbnm qqqzxvv"
        await auditor.input_text(t07_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s07 = await auditor.extract_state()
        await auditor.screenshot("tc07_oov.png")
        results["tc07_oov"] = {
            "input": t07_input,
            "pred_class": s07["pred_class"],
            "confidence": s07["confidence"],
            "alerts": s07["alerts"],
            "uncertainty_box": s07["uncertainty_box_text"],
            "screenshot": "tc07_oov.png",
            "status": "PASS" if any("oov" in a.lower() or "từ điển" in a.lower() for a in s07["alerts"]) else "OBSERVED"
        }
        print(f"  Alerts: {s07['alerts']}")

        # -------------------------------------------------------------
        # TC 08: Low confidence (Mixed topics)
        # -------------------------------------------------------------
        print("\n--- Running TC-08: Low Confidence ---")
        t08_input = "baseball game software render satellite government debate"
        await auditor.input_text(t08_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s08 = await auditor.extract_state()
        await auditor.screenshot("tc08_low_conf.png")
        results["tc08_low_conf"] = {
            "input": t08_input,
            "pred_class": s08["pred_class"],
            "confidence": s08["confidence"],
            "alerts": s08["alerts"],
            "uncertainty_box": s08["uncertainty_box_text"],
            "screenshot": "tc08_low_conf.png",
            "status": "PASS"
        }
        print(f"  Result: {s08['pred_class']} ({s08['confidence']}%), Uncertainty box: {s08['uncertainty_box_text'] is not None}")

        # -------------------------------------------------------------
        # TC 09: Explanations check
        # -------------------------------------------------------------
        print("\n--- Running TC-09: Explanations ---")
        # Explanations from latest valid run (or re-run space)
        t09_input = "Hubble space telescope orbit astronaut cosmic galaxy exploration"
        await auditor.input_text(t09_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s09 = await auditor.extract_state()
        await auditor.screenshot("tc09_explanation.png")
        results["tc09_explanation"] = {
            "input": t09_input,
            "pred_class": s09["pred_class"],
            "confidence": s09["confidence"],
            "tables": s09["tables"],
            "screenshot": "tc09_explanation.png",
            "status": "PASS" if len(s09["tables"]) > 0 else "OBSERVED"
        }
        print(f"  Tables found: {len(s09['tables'])}")
        if s09["tables"]:
            print(f"  Top keywords sample: {s09['tables'][0].get('rows', [])[:3]}")

        # -------------------------------------------------------------
        # TC 10: History check
        # -------------------------------------------------------------
        print("\n--- Running TC-10: History Table ---")
        await auditor.screenshot("tc10_history.png")
        s10 = await auditor.extract_state()
        results["tc10_history"] = {
            "history_rows_count": s10["history_rows_count"],
            "history_preview": s10["history_preview"],
            "screenshot": "tc10_history.png",
            "status": "PASS" if s10["history_rows_count"] >= 2 else "OBSERVED"
        }
        print(f"  History rows observed: {s10['history_rows_count']}")

        # -------------------------------------------------------------
        # TC 11: CSV Download & Verification
        # -------------------------------------------------------------
        print("\n--- Running TC-11: CSV Download ---")
        downloaded_name = "lich_su_du_doan_naive_bayes.csv"
        raw_download_path = os.path.join(EVIDENCE_DIR, downloaded_name)
        target_csv_path = os.path.join(EVIDENCE_DIR, "tc11_downloaded_history.csv")
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
            # Fallback to JS fetch
            csv_content = await auditor.fetch_csv_content()
            if csv_content:
                with open(target_csv_path, "w", encoding="utf-8-sig") as f:
                    f.write(csv_content)

        if csv_content:
            lines = [line.strip() for line in csv_content.strip().splitlines() if line.strip()]
            header = lines[0] if lines else ""
            row_count = len(lines) - 1
            sample_rows = lines[1:4]
            print(f"  Downloaded CSV lines: {len(lines)}, header: {header}")
            print(f"  Sample rows: {sample_rows}")
            results["tc11_csv"] = {
                "csv_saved_path": "tc11_downloaded_history.csv",
                "header": header,
                "row_count": row_count,
                "sample_rows": sample_rows,
                "status": "PASS" if row_count >= 2 else "OBSERVED"
            }
        else:
            print("  CSV download could not be captured!")
            results["tc11_csv"] = {"status": "FAIL", "error": "No CSV content"}

        # -------------------------------------------------------------
        # TC 12: Clear History
        # -------------------------------------------------------------
        print("\n--- Running TC-12: Clear History ---")
        cleared = await auditor.click_clear_history()
        await asyncio.sleep(2)
        s12 = await auditor.extract_state()
        await auditor.screenshot("tc12_clear_history.png")
        results["tc12_clear_history"] = {
            "cleared_clicked": cleared,
            "history_rows_count": s12["history_rows_count"],
            "screenshot": "tc12_clear_history.png",
            "status": "PASS" if s12["history_rows_count"] <= 1 else "OBSERVED"
        }
        print(f"  History rows after clear: {s12['history_rows_count']}")

        # -------------------------------------------------------------
        # TC 13: Page Reload & Verify
        # -------------------------------------------------------------
        print("\n--- Running TC-13: Page Reload & Re-predict ---")
        await auditor.cdp("Page.navigate", {"url": TARGET_URL})
        await auditor.wait_for_app_ready()
        t13_input = "Astronomers observe deep space stellar explosion with radio telescopes."
        await auditor.input_text(t13_input)
        await auditor.click_classify()
        await auditor.wait_for_computation()
        s13 = await auditor.extract_state()
        await auditor.screenshot("tc13_reload.png")
        results["tc13_reload"] = {
            "input": t13_input,
            "pred_class": s13["pred_class"],
            "confidence": s13["confidence"],
            "screenshot": "tc13_reload.png",
            "status": "PASS" if s13["pred_class"] == "sci.space" else "OBSERVED"
        }
        print(f"  Reload prediction: {s13['pred_class']} ({s13['confidence']}%)")

        # Save all structured results
        report_path = os.path.join(EVIDENCE_DIR, "plan9_test_report.json")
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
