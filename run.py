#!/usr/bin/env python3
"""Local server for the Soaring Meteogram.

Starts a local server and opens the page in your browser. Serves src/soaring-meteogram.html and passes the NATS UK PIB (NOTAM) file
through at /PIB.xml, because the NATS site does not let a web page read it directly.
Uses only the Python 3 standard library.

Run:   python3 run.py        (Mac: double-click Soaring Meteogram.command; Windows: py run.py)
Stop:  Ctrl+C in the terminal window.
"""
import http.server
import os
import threading
import time
import webbrowser
import urllib.request

PIB_URL = os.environ.get("PIB_URL", "https://pibs.nats.co.uk/operational/pibs/PIB.xml")
PORT = int(os.environ.get("PORT", "8000"))
CACHE_SECONDS = 600
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
cache = {"at": 0.0, "body": b""}


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HERE, **kwargs)

    def do_GET(self):
        if self.path.split("?")[0] != "/PIB.xml":
            return super().do_GET()
        try:
            if not cache["body"] or time.time() - cache["at"] > CACHE_SECONDS:
                req = urllib.request.Request(PIB_URL, headers={"User-Agent": "soaring-meteogram/1.0"})
                with urllib.request.urlopen(req, timeout=30) as r:
                    cache["body"] = r.read()
                    cache["at"] = time.time()
        except Exception as e:  # serve the last good copy if there is one
            if not cache["body"]:
                self.send_error(502, "Could not fetch the PIB: %s" % e)
                return
        body = cache["body"]
        self.send_response(200)
        self.send_header("Content-Type", "application/xml; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    # Try the usual port first so saved settings stay put (browsers store them per address).
    server = None
    for port in [PORT] + list(range(PORT + 1, PORT + 20)):
        try:
            server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
            break
        except OSError:
            continue
    if server is None:
        raise SystemExit("No free port found near %d" % PORT)
    url = "http://localhost:%d/soaring-meteogram.html" % port
    print("Soaring Meteogram running at %s\nLeave this window open while you use it. Ctrl+C to stop." % url)
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
