from fastapi import Request, Response
from fastapi_csrf_protect import CsrfProtect

from app.middleware.base_middleware import BaseMiddleware


csrf_protect = CsrfProtect()


class VerifyCsrfMiddleware(BaseMiddleware):
    '''
    Verify a CSRF token.
    '''
    
    async def execute(self, request: Request, response: Response):
        if request.method not in ["POST", "PUT", "PATCH", "DELETE"]:
            return response
        
        await csrf_protect.validate_csrf(request)
        
        csrf_protect.unset_csrf_cookie(response)
    
        return response
