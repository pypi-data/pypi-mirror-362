# fastapi_watchlog_apm/middleware.py

import time
import tracemalloc
from starlette.middleware.base import BaseHTTPMiddleware
from .collector import collect_request

class WatchlogAPMMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, service: str):
        super().__init__(app)
        self.service = service

    async def dispatch(self, request, call_next):
        path = request.url.path
        method = request.method

        tracemalloc.start()
        start_time = time.time()

        try:
            response = await call_next(request)
            status_code = response.status_code
        except Exception:
            status_code = 500
            raise
        finally:
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            collect_request(
                service=self.service,
                path=path,
                method=method,
                status_code=status_code,
                duration=(end_time - start_time) * 1000,
                memory={
                    "rss": None,
                    "heapUsed": current,
                    "heapTotal": peak,
                }
            )

        return response
