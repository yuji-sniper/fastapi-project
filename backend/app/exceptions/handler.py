from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse


def setup_exception_handlers(app: FastAPI):
    '''
    Setup exception handlers.
    '''
    app.add_exception_handler(HTTPException, http_exception_handler)


def http_exception_handler(request: Request, exc: HTTPException):
    '''
    Handle HTTP exceptions.
    '''
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )
