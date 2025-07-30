import time
import tracemalloc
from starlette.requests import Request
from .collector import collect_request

class WatchlogAPMMiddleware:
    def __init__(self, app, service: str):
        self.app = app
        self.service = service

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method = scope["method"]
        status_code = 500
        current = peak = 0

        tracemalloc.start()
        start_time = time.time()

        async def send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)

        # اجرای اپلیکیشن FastAPI
        await self.app(scope, receive, send_wrapper)

        # حالا مسیر resolve شده در scope قرار داره
        end_time = time.time()
        request = Request(scope, receive=receive)
        route_path = request.scope.get("route").path if request.scope.get("route") else scope.get("path")

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        duration = (end_time - start_time) * 1000

        try:
            collect_request(
                service=self.service,
                path=route_path,
                method=method,
                status_code=status_code,
                duration=duration,
                memory={
                    "heapUsed": current,
                    "heapTotal": peak
                }
            )
        except:
            pass  # silent fail, no log

        
