from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from routes import ROUTES

class Handler(BaseHTTPRequestHandler):
    def handle_request(self):
        method = self.command
        path = self.path

        handler = ROUTES.get(method, {}).get(path)

        if not handler:
            self._send(404, {"message": "Not found"})
            return

        body = {}
        if method == "POST":
            length = int(self.headers.get("Content-Length", 0))
            if length:
                body = json.loads(self.rfile.read(length))

        result = handler(body)
        self._send(result["status"], result)

    def _send(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_POST(self): self.handle_request()
    def do_GET(self): self.handle_request()

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), Handler)
    server.serve_forever()