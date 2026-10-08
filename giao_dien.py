#!/usr/bin/env python
"""Giao diện chat cho trợ lý Excel — kiểu Claude/Gemini (web local).

    python giao_dien.py            # mở http://127.0.0.1:8765
    python giao_dien.py --port N

Backend gọi `pi -p --mode json` và stream `text_delta` về browser qua SSE.
Mỗi cuộc trò chuyện = 1 session riêng (pi tự lưu trong .pi/web_sessions/).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
SESSION_DIR = HERE / ".pi" / "web_sessions"
PI = shutil.which("pi") or "pi"


def pi_env():
    e = os.environ.copy()
    e["PI_CODING_AGENT_DIR"] = str(HERE)  # nạp AGENTS.md + skills + .pi/agents
    e["PYTHONIOENCODING"] = "utf-8"
    e["PYTHONUTF8"] = "1"
    return e


def _title_of(path: Path) -> str:
    try:
        with path.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    ev = json.loads(line)
                except Exception:
                    continue
                m = ev.get("message") or {}
                if m.get("role") == "user":
                    txt = "".join(c.get("text", "") for c in (m.get("content") or []) if isinstance(c, dict))
                    if txt.strip():
                        return txt.strip().replace("\n", " ")[:70]
    except Exception:
        pass
    return path.stem


def list_convs():
    if not SESSION_DIR.exists():
        return []
    files = sorted(SESSION_DIR.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    return [{"id": f.stem, "title": _title_of(f), "mtime": f.stat().st_mtime} for f in files[:40]]


def history_of(conv: str):
    """Tin nhắn cũ của 1 cuộc trò chuyện (để hiện lại khi mở)."""
    if not SESSION_DIR.exists():
        return []
    hits = list(SESSION_DIR.glob(f"*{conv}.jsonl"))
    if not hits:
        return []
    out = []
    with hits[0].open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                ev = json.loads(line)
            except Exception:
                continue
            if ev.get("type") != "message_end":
                continue
            m = ev.get("message") or {}
            role = m.get("role")
            if role not in ("user", "assistant"):
                continue
            txt = "".join(c.get("text", "") for c in (m.get("content") or []) if isinstance(c, dict))
            if txt.strip():
                out.append({"role": role, "text": txt})
    return out


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):  # im lặng
        pass

    def _send(self, code, ctype, body: bytes):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(code, "application/json; charset=utf-8", json.dumps(obj, ensure_ascii=False).encode("utf-8"))

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            f = HERE / "giao_dien.html"
            if not f.exists():
                return self._send(500, "text/plain; charset=utf-8", b"Thieu file giao_dien.html")
            return self._send(200, "text/html; charset=utf-8", f.read_bytes())
        if path == "/api/convs":
            return self._json(list_convs())
        if path == "/api/history":
            q = self.path.split("?")[1] if "?" in self.path else ""
            conv = q.split("conv=")[-1] if "conv=" in q else ""
            return self._json(history_of(conv))
        return self._send(404, "text/plain; charset=utf-8", b"Not found")

    def do_POST(self):
        if self.path.split("?")[0] != "/api/chat":
            return self._send(404, "text/plain", b"Not found")
        n = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._send(400, "text/plain", b"Bad JSON")
        msg = (body.get("message") or "").strip()
        conv = (body.get("conv") or "").strip() or f"web-{int(time.time())}"
        if not msg:
            return self._send(400, "text/plain", b"Empty message")
        SESSION_DIR.mkdir(parents=True, exist_ok=True)

        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "close")
        self.end_headers()

        def sse(obj):
            try:
                self.wfile.write(("data: " + json.dumps(obj, ensure_ascii=False) + "\n\n").encode("utf-8"))
                self.wfile.flush()
            except Exception:
                pass

        sse({"type": "start", "conv": conv})
        cmd = [PI, "-p", "--mode", "json", "--session-id", conv, "--session-dir", str(SESSION_DIR), msg]
        try:
            p = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace",
                env=pi_env(), cwd=str(HERE),
            )
            for line in p.stdout:
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = json.loads(line)
                except Exception:
                    continue
                ame = ev.get("assistantMessageEvent") or {}
                t = ame.get("type")
                if t == "text_delta":
                    sse({"type": "delta", "text": ame.get("delta", "")})
                elif t == "thinking_delta":
                    sse({"type": "thinking"})
            p.wait()
        except FileNotFoundError:
            sse({"type": "error", "text": "Khong tim thay lenh 'pi'. Chay CaiDat.bat truoc."})
        except Exception as e:
            sse({"type": "error", "text": str(e)})
        sse({"type": "done"})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-browser", action="store_true")
    a = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), Handler)
    url = f"http://127.0.0.1:{a.port}"
    print(f"Giao dien chay tai: {url}   (Ctrl+C de dung)")
    if not a.no_browser:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nDa dung.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
