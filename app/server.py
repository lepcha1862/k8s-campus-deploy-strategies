
"""Campus Notice Board API — CTE412 Practical 15."""

import json
import os
import socket
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# The Docker image supplies these environment variables.
VERSION = os.getenv("APP_VERSION", "1.0.0")
STUDENT_ID = os.getenv("STUDENT_ID", "02230125")
FEATURE_PINNED = os.getenv("FEATURE_PINNED", "false").lower() == "true"

PORT = 8080
START_TIME = time.monotonic()

# All three release images use this application source.
NOTICES = [
    {
        "id": 1,
        "title": "Examination Schedule",
        "message": "Check the updated examination timetable."
    },
    {
        "id": 2,
        "title": "Library Notice",
        "message": "The library will remain open until 10 PM."
    },
    {
        "id": 3,
        "title": "Campus Event",
        "message": "Student orientation begins on Monday."
    }
]

CATEGORIES = {
    1: "Academic",
    2: "Facilities",
    3: "Events"
}


class NoticeHandler(BaseHTTPRequestHandler):

    def send_json(self, status, data):
        body = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?", 1)[0]

        if path == "/version":
            self.send_json(200, {
                "version": VERSION,
                "student": STUDENT_ID,
                "pod": socket.gethostname()
            })

        elif path == "/notices":
            notices = [notice.copy() for notice in NOTICES]

            if VERSION in ("1.1.0", "1.2.0-broken"):
                for notice in notices:
                    notice["category"] = CATEGORIES[notice["id"]]
                    notice["pinned"] = notice["id"] == 3

                if FEATURE_PINNED:
                    notices.sort(
                        key=lambda notice: not notice["pinned"]
                    )

                self.send_json(200, {
                    "notices": notices,
                    "pinnedFirst": FEATURE_PINNED
                })
            else:
                self.send_json(200, {"notices": notices})

        elif path == "/healthz":
            elapsed = time.monotonic() - START_TIME

            if VERSION == "1.2.0-broken":
                self.send_json(503, {
                    "status": "unhealthy",
                    "reason": "simulated release failure"
                })

            elif elapsed < 5:
                self.send_json(503, {
                    "status": "starting",
                    "reason": "five-second warm-up"
                })

            else:
                self.send_json(200, {
                    "status": "healthy"
                })

        else:
            self.send_json(404, {"error": "Not found"})


if __name__ == "__main__":
    if VERSION not in ("1.0.0", "1.1.0", "1.2.0-broken"):
        raise ValueError(f"Unsupported version: {VERSION}")

    server = ThreadingHTTPServer(("0.0.0.0", PORT), NoticeHandler)
    print(
        f"Campus Notice Board {VERSION} listening on {PORT}",
        flush=True
    )
    server.serve_forever()
