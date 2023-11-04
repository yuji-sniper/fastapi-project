from decouple import config
from pydantic import BaseModel


class Csrf(BaseModel):
    csrf_token: str


class CsrfSettings(BaseModel):
    secret_key: str = config("SECRET_KEY")
    cookie_samesite: str = "lax" # TODO: httpsにしたらnoneにする
    cookie_secure: bool = False # TODO: httpsにしたらtrueにする
