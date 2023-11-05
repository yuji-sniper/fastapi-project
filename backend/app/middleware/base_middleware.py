from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastapi_csrf_protect.exceptions import CsrfProtectError
from starlette.middleware.base import BaseHTTPMiddleware


class BaseMiddleware(BaseHTTPMiddleware):
    '''
    Base middleware.
    '''
    
    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
        self.options = kwargs
    
    
    async def dispatch(self, request, call_next):
        '''
        Dispatch middleware.
        '''
        response = await call_next(request)
        try:
            response = await self.execute(request, response)
        except Exception as e:
            return self.handle_error(e)
        return response
    
    
    async def execute(self, request: Request, response: Response):
        '''
        Execute middleware.
        '''
        raise NotImplementedError("Request processing needs to be implemented.")
    
    
    def handle_error(self, e: Exception):
        '''
        Handle an error.
        '''
        if (isinstance(e, CsrfProtectError)):
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.message}
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"}
            )
