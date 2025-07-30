from fastapi import Request
from fastapi.responses import HTMLResponse

from starlette.middleware.base import BaseHTTPMiddleware


class PermissionMiddleware:
    def __init__(self, app):
        self.app = app  # Store FastAPI application

    async def __call__(self, scope, receive, send):
        # Check if this is an HTTP request
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Create Request object for convenience
        request = Request(scope, receive)

        # Check if user is authenticated
        if not hasattr(request, "user") or not getattr(request.user, "is_authenticated", False):
            response = HTMLResponse('Forbidden', status_code=403)
            await response(scope, receive, send)
            return

        # Check if display_name matches user_id from path_params
        if request.user.display_name == request.path_params.get('user_id'):
            # If check passes, continue processing
            await self.app(scope, receive, send)
            return

        # If check fails, return 403 error
        response = HTMLResponse('Forbidden', status_code=403)
        await response(scope, receive, send)
