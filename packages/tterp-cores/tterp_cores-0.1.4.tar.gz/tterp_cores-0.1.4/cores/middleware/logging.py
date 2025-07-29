"""
Logging middleware - Ghi log các request và response
"""

import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from cores.logger.logging import ApiLogger


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware để ghi log các request và response

    Ghi log thời gian xử lý, method, path, status code và thời gian phản hồi
    """

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        """
        Xử lý request và ghi log

        Args:
            request: Request object
            call_next: Hàm xử lý request tiếp theo

        Returns:
            Response object
        """
        start_time = time.time()

        # Log request
        ApiLogger.info(f"Request: {request.method} {request.url.path}")

        # Xử lý request
        response = await call_next(request)

        # Tính thời gian xử lý
        process_time = time.time() - start_time

        # Log response
        ApiLogger.info(
            f"Response: {request.method} {request.url.path} "
            f"- Status: {response.status_code} "
            f"- Time: {process_time:.4f}s"
        )

        return response
