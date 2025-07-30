# fastapi_watchlog_apm/error_handler.py

from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from .collector import collect_request

def apm_exception_handler(app: FastAPI, service: str):
    @app.exception_handler(Exception)
    async def handle_exception(request: Request, exc: Exception):
        collect_request(
            service=service,
            path=request.url.path,
            method=request.method,
            status_code=500,
            duration=0,
            memory={
                "rss": None,
                "heapUsed": 0,
                "heapTotal": 0
            }
        )
        raise exc  # Let FastAPI handle displaying the error normally
