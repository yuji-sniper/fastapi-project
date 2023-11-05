from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse


def http_exception_handler(request: Request, exc: HTTPException):
    '''
    Handle HTTP exceptions.
    '''
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
   
   
def setup_exception_handlers(app: FastAPI):
    '''
    Setup exception handlers.
    '''
    app.add_exception_handler(HTTPException, http_exception_handler)
