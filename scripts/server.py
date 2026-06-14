import json
import os
import subprocess
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "static"
MCP = ROOT / "mcp" / "wiki_mcp_server.py"
AGENT = ROOT / "scripts" / "wiki_agent.py"
sys.stdout.reconfigure(encoding="utf-8")


def run_mcp_tool(name, arguments):
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": name, "arguments": arguments},
    }
    proc = subprocess.run(
        [sys.executable, str(MCP)],
        input=json.dumps(request, ensure_ascii=False),
        text=True,
        capture_output=True,
        encoding="utf-8",
        cwd=str(ROOT),
        check=False,
    )
    payload = json.loads(proc.stdout)
    if "error" in payload:
        raise RuntimeError(payload["error"]["message"])
    return payload["result"]


def run_agent(question):
    proc = subprocess.run(
        [sys.executable, str(AGENT), question],
        text=True,
        capture_output=True,
        encoding="utf-8",
        cwd=str(ROOT),
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or "Agent failed")
    return json.loads(proc.stdout)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC), **kwargs)

    def send_json(self, payload, status=200):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(length).decode("utf-8") or "{}")

    def do_GET(self):
        try:
            if self.path == "/api/pages":
                return self.send_json(run_mcp_tool("list_pages", {}))
            if self.path.startswith("/api/page/"):
                slug = self.path.rsplit("/", 1)[-1]
                return self.send_json(run_mcp_tool("get_page", {"slug": slug}))
            return super().do_GET()
        except Exception as exc:
            return self.send_json({"error": str(exc)}, 500)

    def do_POST(self):
        try:
            payload = self.read_json()
            if self.path == "/api/search":
                return self.send_json(run_mcp_tool("search_pages", {"query": payload.get("query", "")}))
            if self.path == "/api/chat":
                return self.send_json(run_agent(payload.get("question", "")))
            return self.send_json({"error": "Not found"}, 404)
        except Exception as exc:
            return self.send_json({"error": str(exc)}, 500)


def main():
    port = int(os.environ.get("PORT", "8765"))
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"ML Wiki MCP Tool running at http://127.0.0.1:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
