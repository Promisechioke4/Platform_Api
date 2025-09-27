import json
import os
import time
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin

# Store logs inside middleware folder (JSON lines file)
LOG_FILE = os.path.join(os.path.dirname(__file__), "api_logs.jsonl")


class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Capture request start time
        request.start_time = time.time()

    def process_response(self, request, response):
        try:
            start = getattr(request, "start_time", time.time())
            end = time.time()
            duration = int((end - start) * 1000)

            log_data = {
                "user": request.user.username if request.user.is_authenticated else "anonymous",
                "path": request.path,
                "method": request.method,
                "status_code": response.status_code,
                "start_time": datetime.utcfromtimestamp(start).isoformat() + "Z",
                "end_time": datetime.utcfromtimestamp(end).isoformat() + "Z",
                "duration_ms": duration,
            }

            # Append logs as JSON lines
            with open(LOG_FILE, "a") as f:
                f.write(json.dumps(log_data) + "\n")

        except Exception as e:
            print("⚠️ Logging error:", e)

        return response
