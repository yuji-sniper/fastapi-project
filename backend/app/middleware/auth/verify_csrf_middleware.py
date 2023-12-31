from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from starlette.middleware.base import BaseHTTPMiddleware


csrf_protect = CsrfProtect()


class VerifyCsrfMiddleware(BaseHTTPMiddleware):
    '''
    Verify a CSRF token.
    '''
    
    async def dispatch(self, request, call_next):
        if request.method not in ["POST", "PUT", "PATCH", "DELETE"]:
            return await call_next(request)
        
        try:
            await csrf_protect.validate_csrf(request)
        except CsrfProtectError as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"message": e.message}
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"message": "Internal Server Error"}
            )
        
        response = await call_next(request)
        
        csrf_protect.unset_csrf_cookie(response)
    
        return response
