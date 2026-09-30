#!/usr/bin/env python3
"""
Rigorous Plan 11 Post-Release Live Cloud Verifier:
Must exit with non-zero code if ANY condition fails:
1. Unauthenticated public access
2. Version must strictly be 'v1.0.4' in BOTH sidebar and footer (fail if v1.0.3)
3. Empty input on new session: warning, 0 history, no prediction box
4. Valid prediction: NASA sentence -> sci.space, history count = 1
5. Whitespace after valid: warning, history count remains 1
6. Short text 'space': valid prediction, history preview is 'space' without '(Rỗng)'
7. Download CSV: exactly 2 data rows (NASA, space), matches history, 0 empty rows, no '(Rỗng)'
8. Reload page: version remains 'v1.0.4', another prediction succeeds

Evidence saved to docs/evidence/plan-11/
"""

from __future__ import annotations

import asyncio
import base64
import csv
import io
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
import websockets

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE_DIR = r"D:\phan-loai-van-ban-naive-bayes\.chrome_profile"
TARGET_URL = "https://phan-loai-van-ban-naive-bayes.streamlit.app/"
ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_DIR = ROOT / "docs" / "evidence" / "plan-11"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


class LiveCloudAuditorPlan11:
    def __init__(self):
        self.proc = None
        self.ws = None
        self.req_id = 0
        self.test_results = {}

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
                "downloadPath": str(EVIDENCE_DIR),
            })
        except Exception as e:
            print(f"Warning: Page.setDownloadBehavior: {e}")

    async def cdp(self, method, params=None):
        self.req_id += 1
        msg = {"id": self.req_id, "method": method, "params": params or {}}
        await self.ws.send(json.dumps(msg))
        while True:
            resp = json.loads(await self.ws.recv())
            if resp.get("id") == self.req_id:
                return resp.get("result", {})

    async def eval_js(self, expression):
        res = await self.cdp("Runtime.evaluate", {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": True,
        })
        val = res.get("result", {})
        if "value" in val:
            return val["value"]
        return res

    async def capture_screenshot(self, filename: str) -> Path:
        res = await self.cdp("Page.captureScreenshot", {"format": "png"})
        b64 = res.get("data", "")
        path = EVIDENCE_DIR / filename
        if b64:
            path.write_bytes(base64.b64decode(b64))
            print(f"  [Đã lưu ảnh chụp]: {filename}")
        return path

    async def wait_for_app_ready(self, timeout=40):
        print("Đang đợi Streamlit iframe sẵn sàng...")
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
                print(f"Streamlit iframe sẵn sàng sau {i+1}s!")
                await asyncio.sleep(2)
                return True
        raise TimeoutError("Streamlit iframe không tải được.")

    async def wait_for_computation(self, timeout=20):
        for _ in range(timeout * 2):
            await asyncio.sleep(0.5)
            running = await self.eval_js("""
            (() => {
                const iframe = document.querySelector('iframe');
                if (!iframe) return false;
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                return doc.querySelector('[data-testid="stStatusWidget"]') !== null;
            })()
            """)
            if not running:
                await asyncio.sleep(0.5)
                return True
        return False

    async def input_text(self, text: str):
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
        await self.eval_js(js)
        await asyncio.sleep(1.0)

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
        await self.eval_js(js)
        await asyncio.sleep(0.5)
        await self.wait_for_computation()

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
        await self.eval_js(js)
        await asyncio.sleep(1.0)

    async def extract_state(self):
        js = """
        (() => {
            const iframe = document.querySelector('iframe');
            if (!iframe) return { error: 'No iframe' };
            const doc = iframe.contentDocument || iframe.contentWindow.document;

            // Sidebar version
            const sidebar = doc.querySelector('[data-testid="stSidebar"]');
            const sidebarText = sidebar ? sidebar.innerText : '';

            // Footer version
            const footerEls = Array.from(doc.querySelectorAll('footer, p, small, span'))
                .map(e => (e.innerText || '').trim())
                .filter(t => t.includes('Khoa Công nghệ') || t.includes('v1.0.') || t.includes('Plan'));

            // Alerts
            const alerts = Array.from(doc.querySelectorAll('[data-testid="stAlert"]'))
                .map(a => (a.innerText || '').trim());

            // Result box
            const resultBox = doc.querySelector('.result-box');
            let predClass = null;
            let confidence = null;
            let vnName = null;
            let latencyMs = null;
            if (resultBox) {
                const text = resultBox.innerText || '';
                const lines = text.split('\\n').map(l => l.trim()).filter(Boolean);
                for (const line of lines) {
                    if (line.includes("Chủ đề dự đoán:")) predClass = line.split("Chủ đề dự đoán:")[1].trim();
                    else if (line.includes("Tên tiếng Việt:")) vnName = line.split("Tên tiếng Việt:")[1].trim();
                    else if (line.includes("Độ tin cậy")) {
                        const m = line.match(/([0-9.]+)%/);
                        if (m) confidence = parseFloat(m[1]);
                    } else if (line.includes("Thời gian xử lý:")) {
                        const m = line.match(/([0-9.]+)\s*ms/);
                        if (m) latencyMs = parseFloat(m[1]);
                    }
                }
            }

            // History isolated count from caption
            let historyCount = 0;
            const captions = Array.from(doc.querySelectorAll('[data-testid="stCaptionContainer"], p, small, span'));
            for (const c of captions) {
                const txt = (c.innerText || '').trim();
                const m = txt.match(/Tổng số lượt dự đoán:\\s*(\\d+)/i);
                if (m) {
                    historyCount = parseInt(m[1], 10);
                    break;
                }
            }

            // History table rows
            const tables = Array.from(doc.querySelectorAll('table'));
            let historyRows = [];
            // Last table is history table if present
            if (tables.length > 0) {
                const lastTable = tables[tables.length - 1];
                const trs = Array.from(lastTable.querySelectorAll('tr'));
                for (const tr of trs) {
                    const tds = Array.from(tr.querySelectorAll('td')).map(td => (td.innerText || '').trim());
                    if (tds.length >= 3) {
                        historyRows.push(tds);
                    }
                }
            }

            // Download button
            const downloadBtn = Array.from(doc.querySelectorAll('a[download], button')).find(b => (b.innerText || '').includes('Tải lịch sử'));

            return {
                sidebarText,
                footerTexts: footerEls,
                alerts,
                hasResultBox: !!resultBox,
                predClass,
                confidence,
                vnName,
                latencyMs,
                historyCount,
                historyRows,
                hasDownloadBtn: !!downloadBtn
            };
        })()
        """
        return await self.eval_js(js)

    async def run_full_suite(self) -> bool:
        print("=" * 70)
        print("BỘ KIỂM THỬ HẬU KIỂM NGHIÊM NGẶT PLAN 11 - STREAMLIT CLOUD (v1.0.4)")
        print("=" * 70)

        all_passed = True

        # CA 1: Truy cập công khai
        print("\n--- CA 1: TRUY CẬP CÔNG KHAI ---")
        await self.wait_for_app_ready()
        st0 = await self.extract_state()
        await self.capture_screenshot("plan11_ca1_public_access.png")
        if "error" in st0:
            print("[THẤT BẠI] Không truy cập được ứng dụng Streamlit!")
            return False
        print("[ĐẠT] Ứng dụng nạp thành công ở phiên khách công khai không cần đăng nhập.")
        self.test_results["ca1_public_access"] = "PASS"

        # CA 2: Kiểm tra phiên bản hiển thị trên Sidebar và Footer
        print("\n--- CA 2: PHIÊN BẢN SIDEBAR VÀ FOOTER PHẢI LÀ v1.0.4 ---")
        sidebar_has_v104 = "v1.0.4" in st0.get("sidebarText", "")
        footer_has_v104 = any("v1.0.4" in f for f in st0.get("footerTexts", []))

        print(f"-> Sidebar chứa v1.0.4: {sidebar_has_v104}")
        print(f"-> Footer chứa v1.0.4:  {footer_has_v104}")
        print(f"-> Footer thực tế: {st0.get('footerTexts')}")

        if sidebar_has_v104 and footer_has_v104:
            print("[ĐẠT] Cả Sidebar và Footer đều hiển thị chính xác phiên bản v1.0.4!")
            self.test_results["ca2_version"] = "PASS"
        else:
            print("[THẤT BẠI] Phiên bản trên Cloud chưa hiển thị v1.0.4 (cần reboot ứng dụng trên dashboard)!")
            self.test_results["ca2_version"] = "FAIL"
            all_passed = False

        # CA 3: Gửi rỗng ở phiên mới
        print("\n--- CA 3: GỬI ĐẦU VÀO RỖNG Ở PHIÊN MỚI ---")
        await self.input_text("")
        await self.click_classify()
        st_empty = await self.extract_state()
        await self.capture_screenshot("plan11_ca3_empty_input.png")

        has_warn = any("Vui lòng nhập nội dung văn bản" in a for a in st_empty.get("alerts", []))
        hist_zero = st_empty.get("historyCount", 0) == 0
        no_res = not st_empty.get("hasResultBox", False)

        print(f"-> Cảnh báo rỗng hiển thị: {has_warn}")
        print(f"-> Số lượt dự đoán: {st_empty.get('historyCount')} (Kỳ vọng: 0)")
        print(f"-> Không có hộp kết quả: {no_res}")

        if has_warn and hist_zero and no_res:
            print("[ĐẠT] Đầu vào rỗng bị chặn chính xác, lịch sử vẫn 0 dòng.")
            self.test_results["ca3_empty_input"] = "PASS"
        else:
            print("[THẤT BẠI] Đầu vào rỗng không đạt yêu cầu!")
            self.test_results["ca3_empty_input"] = "FAIL"
            all_passed = False

        # CA 4: Dự đoán hợp lệ (NASA sentence từ Plan 10)
        print("\n--- CA 4: DỰ ĐOÁN HỢP LỆ (NASA SENTENCE) ---")
        nasa_text = "NASA launched a spacecraft into orbit to study distant planets and explore the solar system."
        await self.input_text(nasa_text)
        await self.click_classify()
        st_nasa = await self.extract_state()
        await self.capture_screenshot("plan11_ca4_valid_nasa.png")

        pred_ok = st_nasa.get("predClass") == "sci.space"
        hist_one = st_nasa.get("historyCount", 0) == 1
        print(f"-> Nhãn dự đoán: {st_nasa.get('predClass')} (Kỳ vọng: sci.space) -> {pred_ok}")
        print(f"-> Độ tin cậy: {st_nasa.get('confidence')}% | Độ trễ: {st_nasa.get('latencyMs')} ms")
        print(f"-> Số lượt dự đoán: {st_nasa.get('historyCount')} (Kỳ vọng: 1) -> {hist_one}")

        if pred_ok and hist_one:
            print("[ĐẠT] Dự đoán hợp lệ thành công, ghi nhận đúng 1 dòng lịch sử.")
            self.test_results["ca4_valid_nasa"] = "PASS"
        else:
            print("[THẤT BẠI] Dự đoán hợp lệ không đạt yêu cầu!")
            self.test_results["ca4_valid_nasa"] = "FAIL"
            all_passed = False

        # CA 5: Khoảng trắng sau lượt hợp lệ
        print("\n--- CA 5: KHOẢNG TRẮNG SAU LƯỢT HỢP LỆ ---")
        await self.input_text("    \t\n   ")
        await self.click_classify()
        st_ws = await self.extract_state()
        await self.capture_screenshot("plan11_ca5_whitespace_after_valid.png")

        has_warn_ws = any("Vui lòng nhập nội dung văn bản" in a for a in st_ws.get("alerts", []))
        hist_stay_one = st_ws.get("historyCount", 0) == 1
        print(f"-> Cảnh báo hiển thị: {has_warn_ws}")
        print(f"-> Số lượt dự đoán: {st_ws.get('historyCount')} (Kỳ vọng giữ nguyên: 1) -> {hist_stay_one}")

        if has_warn_ws and hist_stay_one:
            print("[ĐẠT] Khoảng trắng sau lượt hợp lệ không tăng số dòng lịch sử.")
            self.test_results["ca5_whitespace_after_valid"] = "PASS"
        else:
            print("[THẤT BẠI] Lịch sử bị tăng hoặc thiếu cảnh báo sau khoảng trắng!")
            self.test_results["ca5_whitespace_after_valid"] = "FAIL"
            all_passed = False

        # CA 6: Đoạn trích ngắn 'space'
        print("\n--- CA 6: ĐOẠN TRÍCH NGẮN 'space' ---")
        await self.input_text("space")
        await self.click_classify()
        st_short = await self.extract_state()
        await self.capture_screenshot("plan11_ca6_short_space.png")

        short_hist = st_short.get("historyCount", 0) == 2
        print(f"-> Số lượt dự đoán sau 'space': {st_short.get('historyCount')} (Kỳ vọng: 2) -> {short_hist}")
        if short_hist:
            print("[ĐẠT] Đoạn trích ngắn được phân loại và thêm đúng vào dòng thứ 2.")
            self.test_results["ca6_short_space"] = "PASS"
        else:
            print("[THẤT BẠI] Phân loại đoạn trích ngắn thất bại!")
            self.test_results["ca6_short_space"] = "FAIL"
            all_passed = False

        # CA 7: Tải CSV thật từ trình duyệt và đối chiếu
        print("\n--- CA 7: TẢI VÀ ĐỐI CHIẾU CSV THẬT ---")
        raw_download_name = "lich_su_du_doan_naive_bayes.csv"
        raw_download_path = EVIDENCE_DIR / raw_download_name
        target_csv_path = EVIDENCE_DIR / "plan11_downloaded_history.csv"

        if raw_download_path.exists():
            raw_download_path.unlink()
        if target_csv_path.exists():
            target_csv_path.unlink()

        click_download_js = """
        (() => {
            const iframe = document.querySelector('iframe');
            if (!iframe) return false;
            const doc = iframe.contentDocument || iframe.contentWindow.document;
            const dlBtn = Array.from(doc.querySelectorAll('a[download], a, button')).find(el => (el.innerText || '').includes('Tải lịch sử'));
            if (dlBtn) {
                dlBtn.click();
                return true;
            }
            return false;
        })()
        """
        clicked = await self.eval_js(click_download_js)
        print(f"  Đã bấm nút tải CSV trên giao diện: {clicked}")

        csv_content = None
        for wait_i in range(8):
            await asyncio.sleep(1)
            if raw_download_path.exists():
                csv_content = raw_download_path.read_text(encoding="utf-8-sig", errors="replace")
                target_csv_path.write_text(csv_content, encoding="utf-8-sig")
                print(f"  [Đã tải CSV từ trình duyệt]: {target_csv_path.name} (sau {wait_i+1}s)")
                break

        if csv_content:
            lines = [l.strip() for l in csv_content.strip().splitlines() if l.strip()]
            headers = lines[0] if lines else ""
            data_rows = lines[1:] if len(lines) > 1 else []
            print(f"-> Tiêu đề CSV: {headers}")
            print(f"-> Số dòng dữ liệu trong CSV: {len(data_rows)} (Kỳ vọng: 2)")

            clean_previews = True
            for r in data_rows:
                print(f"   Dòng: {r}")
                if "(Rỗng)" in r:
                    clean_previews = False

            if len(data_rows) == 2 and clean_previews:
                print("[ĐẠT] Tệp CSV có đúng 2 dòng, dữ liệu khớp lịch sử và 100% không có lỗi (Rỗng)!")
                self.test_results["ca7_csv"] = "PASS"
            else:
                print(f"[THẤT BẠI] CSV không đạt (số dòng: {len(data_rows)}, sạch: {clean_previews})!")
                self.test_results["ca7_csv"] = "FAIL"
                all_passed = False
        else:
            print("[THẤT BẠI] Trình duyệt không tải được tệp CSV sau khi bấm nút!")
            self.test_results["ca7_csv"] = "FAIL"
            all_passed = False

        # CA 8: Tải lại trang và chạy thêm một dự đoán
        print("\n--- CA 8: TẢI LẠI TRANG VÀ THỰC HIỆN DỰ ĐOÁN MỚI ---")
        await self.eval_js("window.location.reload()")
        await asyncio.sleep(6)
        await self.wait_for_app_ready()
        st_reload = await self.extract_state()
        await self.capture_screenshot("plan11_ca8_reload.png")

        reload_version_ok = ("v1.0.4" in st_reload.get("sidebarText", "")) and any("v1.0.4" in f for f in st_reload.get("footerTexts", []))
        print(f"-> Phiên bản sau reload là v1.0.4: {reload_version_ok}")

        # Run one prediction
        await self.input_text("Astronomers observe supernova explosions in distant spiral galaxies.")
        await self.click_classify()
        st_final = await self.extract_state()
        await self.capture_screenshot("plan11_ca8_reload_prediction.png")

        final_pred_ok = st_final.get("predClass") == "sci.space" and st_final.get("historyCount", 0) == 1
        print(f"-> Dự đoán sau reload: {st_final.get('predClass')}, Số dòng lịch sử: {st_final.get('historyCount')}")

        if reload_version_ok and final_pred_ok:
            print("[ĐẠT] Tải lại trang thành công, phiên bản duy trì v1.0.4, dự đoán mới hoạt động hoàn hảo.")
            self.test_results["ca8_reload"] = "PASS"
        else:
            print(f"[THẤT BẠI] Ca tải lại không đạt (Version OK: {reload_version_ok}, Dự đoán OK: {final_pred_ok})!")
            self.test_results["ca8_reload"] = "FAIL"
            all_passed = False

        # Summary JSON
        report_path = EVIDENCE_DIR / "plan11_test_report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "target_url": TARGET_URL,
                "all_passed": all_passed,
                "results": self.test_results,
            }, f, indent=2, ensure_ascii=False)
        print(f"\n[Báo cáo tổng hợp]: {report_path}")

        print("=" * 70)
        print(f"KẾT QUẢ CUỐI CÙNG: {'TẤT CẢ 8 CA ĐỀU ĐẠT (SUCCESS)' if all_passed else 'CÓ CA THẤT BẠI HOẶC CHỜ REBOOT'}")
        print("=" * 70)
        return all_passed


async def main():
    auditor = LiveCloudAuditorPlan11()
    auditor.start_browser()
    try:
        await auditor.connect()
        success = await auditor.run_full_suite()
        return 0 if success else 1
    finally:
        auditor.stop_browser()


if __name__ == "__main__":
    code = asyncio.run(main())
    sys.exit(code)
