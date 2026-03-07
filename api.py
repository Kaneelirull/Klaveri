"""
Minimal scores API server using Python stdlib only.
Listens on 127.0.0.1:3001, proxied from nginx at /api/.

Endpoints:
  GET  /api/scores/<file>.json  -> return JSON object (or {} if missing/corrupt)
  POST /api/scores/<file>.json  -> write JSON body to /data/scores/<file>.json
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

SCORES_DIR = '/data/scores'
PORT = 3001


def _valid_filename(name):
    return name.endswith('.json') and '/' not in name and '..' not in name


class ScoresHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass  # suppress access logs

    def _send_json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def _parse_filename(self):
        # expects /api/scores/<filename>.json
        parts = self.path.split('?')[0].strip('/').split('/')
        if len(parts) == 3 and parts[0] == 'api' and parts[1] == 'scores':
            fn = parts[2]
            if _valid_filename(fn):
                return fn
        return None

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        fn = self._parse_filename()
        if not fn:
            self._send_json(400, {'error': 'invalid path'})
            return
        path = os.path.join(SCORES_DIR, fn)
        try:
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
            self._send_json(200, data)
        except Exception:
            self._send_json(200, {})

    def do_POST(self):
        fn = self._parse_filename()
        if not fn:
            self._send_json(400, {'error': 'invalid path'})
            return
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            data = json.loads(body)
            os.makedirs(SCORES_DIR, exist_ok=True)
            path = os.path.join(SCORES_DIR, fn)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self._send_json(200, {'ok': True})
        except Exception as e:
            self._send_json(500, {'error': str(e)})


if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', PORT), ScoresHandler)
    print(f'Scores API listening on 127.0.0.1:{PORT}')
    server.serve_forever()
