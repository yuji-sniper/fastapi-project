from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError, MissingTokenError

from app.api.v1.router import api_router as v1_router
from app.api.v2.router import api_router as v2_router
from app.middleware.auth.verify_csrf_middleware import VerifyCsrfMiddleware
from app.schemas.csrf import CsrfSettings


app = FastAPI()

app.include_router(v1_router, prefix="/v1")
app.include_router(v2_router, prefix="/v2")


app.add_middleware(CORSMiddleware,
                   allow_origins=['http://localhost:3000'],
                   allow_credentials=True,
                   allow_methods=["POST", "GET", "PUT", "PATCH", "DELETE"],
                   allow_headers=["*"])
app.add_middleware(VerifyCsrfMiddleware)


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
