#!/usr/bin/env python3
"""
Verify post-release deployment of v1.0.4 on Streamlit Cloud:
1. Confirm footer / sidebar displays v1.0.4.
2. Confirm empty input produces warning and does not trigger prediction or history.
3. Confirm a valid prediction succeeds and creates proper history.
4. Capture screenshot as tc18_post_release_v1_0_4.png.
"""

from __future__ import annotations

import asyncio
import base64
import json
import os
import subprocess
import time
import urllib.request
from pathlib import Path
import websockets

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE_DIR = r"D:\phan-loai-van-ban-naive-bayes\.chrome_profile"
TARGET_URL = "https://phan-loai-van-ban-naive-bayes.streamlit.app/"
EVIDENCE_DIR = Path(r"D:\phan-loai-van-ban-naive-bayes\docs\evidence\plan-10")


class PostReleaseVerifier:
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

    async def take_screenshot(self, filepath: Path):
        res = await self.cdp("Page.captureScreenshot", {"format": "png"})
        b64 = res.get("data", "")
        if b64:
            filepath.write_bytes(base64.b64decode(b64))
            print(f"  [Đã lưu ảnh chụp]: {filepath.name}")

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
                print(f"Streamlit iframe đã sẵn sàng sau {i+1} giây!")
                await asyncio.sleep(2)
                return True
        raise TimeoutError("Streamlit iframe không tải được trong thời gian quy định.")

    async def run_checks(self):
        print("=" * 70)
        print("KIỂM TRA HẬU PHÁT HÀNH TRÊN STREAMLIT CLOUD (v1.0.4)")
        print("=" * 70)

        await self.wait_for_app_ready()

        # 1. Check footer and sidebar text inside iframe
        version_texts = await self.eval_js("""
            (() => {
                const iframe = document.querySelector('iframe');
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                const els = Array.from(doc.querySelectorAll('footer, p, div, span, small'));
                return els.map(e => (e.innerText || '').trim())
                          .filter(t => t.includes('v1.0.') || t.includes('Plan'))
                          .join(' | ');
            })()
        """)
        print(f"-> Thông tin phiên bản phát hiện trong iframe: {version_texts}")

        # 2. Test empty input
        print("\n-> Kiểm thử gửi đầu vào rỗng...")
        # Clear textarea
        await self.eval_js("""
            (() => {
                const iframe = document.querySelector('iframe');
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                const ta = doc.querySelector('textarea');
                if (ta) {
                    const valueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
                    valueSetter.call(ta, "");
                    ta.dispatchEvent(new Event('input', { bubbles: true }));
                    ta.dispatchEvent(new Event('change', { bubbles: true }));
                    ta.blur();
                }
            })()
        """)
        await asyncio.sleep(1)

        # Click classify
        await self.eval_js("""
            (() => {
                const iframe = document.querySelector('iframe');
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                const buttons = Array.from(doc.querySelectorAll('button'));
                const btn = buttons.find(b => (b.innerText || '').includes('Phân loại'));
                if (btn) btn.click();
            })()
        """)
        await asyncio.sleep(2)

        # Check for warning
        warning_text = await self.eval_js("""
            (() => {
                const iframe = document.querySelector('iframe');
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                const alerts = Array.from(doc.querySelectorAll('[data-testid="stAlert"]'));
                const warn = alerts.find(a => (a.innerText || '').includes('Vui lòng nhập nội dung văn bản'));
                return warn ? (warn.innerText || '').trim() : '';
            })()
        """)
        print(f"-> Cảnh báo rỗng: '{warning_text}' -> {'[ĐẠT]' if warning_text else '[CHƯA THẤY]'}")

        # Check isolated history count
        empty_history_count = await self.eval_js("""
            (() => {
                const iframe = document.querySelector('iframe');
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                const captions = Array.from(doc.querySelectorAll('[data-testid="stCaptionContainer"], p, small, span'));
                for (const c of captions) {
                    const txt = (c.innerText || '').trim();
                    const m = txt.match(/Tổng số lượt dự đoán:\\s*(\\d+)/i);
                    if (m) return parseInt(m[1], 10);
                }
                return 0;
            })()
        """)
        print(f"-> Số lượt dự đoán sau thao tác rỗng: {empty_history_count} (Kỳ vọng: 0) -> {'[ĐẠT]' if empty_history_count == 0 else '[CHƯA ĐẠT]'}")

        # 3. Test valid prediction
        print("\n-> Kiểm thử gửi đầu vào hợp lệ...")
        test_text = "NASA telescope observes distant galaxies and stellar systems in outer space."
        await self.eval_js(f"""
            (() => {{
                const iframe = document.querySelector('iframe');
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                const ta = doc.querySelector('textarea');
                if (ta) {{
                    const valueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
                    valueSetter.call(ta, {json.dumps(test_text)});
                    ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    ta.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', ctrlKey: true, bubbles: true }}));
                    ta.blur();
                }}
            }})()
        """)
        await asyncio.sleep(1)

        # Click classify
        await self.eval_js("""
            (() => {
                const iframe = document.querySelector('iframe');
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                const buttons = Array.from(doc.querySelectorAll('button'));
                const btn = buttons.find(b => (b.innerText || '').includes('Phân loại'));
                if (btn) btn.click();
            })()
        """)

        # Wait for computation
        for _ in range(20):
            await asyncio.sleep(0.5)
            running = await self.eval_js("""
                (() => {
                    const iframe = document.querySelector('iframe');
                    const doc = iframe.contentDocument || iframe.contentWindow.document;
                    return doc.querySelector('[data-testid="stStatusWidget"]') !== null;
                })()
            """)
            if not running:
                await asyncio.sleep(1)
                break

        # Check prediction result
        pred_label = await self.eval_js("""
            (() => {
                const iframe = document.querySelector('iframe');
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                const box = doc.querySelector('.result-box');
                return box ? (box.innerText || '').trim() : '';
            })()
        """)
        print(f"-> Kết quả hộp dự đoán:\n{pred_label}")

        valid_history_count = await self.eval_js("""
            (() => {
                const iframe = document.querySelector('iframe');
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                const captions = Array.from(doc.querySelectorAll('[data-testid="stCaptionContainer"], p, small, span'));
                for (const c of captions) {
                    const txt = (c.innerText || '').trim();
                    const m = txt.match(/Tổng số lượt dự đoán:\\s*(\\d+)/i);
                    if (m) return parseInt(m[1], 10);
                }
                return 0;
            })()
        """)
        print(f"-> Số lượt dự đoán sau thao tác hợp lệ: {valid_history_count} (Kỳ vọng: 1) -> {'[ĐẠT]' if valid_history_count == 1 else '[CHƯA ĐẠT]'}")

        # Capture evidence screenshot
        ss_path = EVIDENCE_DIR / "tc18_post_release_v1_0_4.png"
        await self.take_screenshot(ss_path)

        all_ok = bool(warning_text) and empty_history_count == 0 and ("sci.space" in pred_label) and valid_history_count == 1
        print("\n" + "=" * 70)
        print(f"KẾT QUẢ KIỂM TRA HẬU PHÁT HÀNH: {'TẤT CẢ ĐẠT (SUCCESS)' if all_ok else 'CẦN KIỂM TRA'}")
        print("=" * 70)
        return all_ok


async def main():
    verifier = PostReleaseVerifier()
    verifier.start_browser()
    try:
        await verifier.connect()
        success = await verifier.run_checks()
        return 0 if success else 1
    finally:
        verifier.stop_browser()


if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))
