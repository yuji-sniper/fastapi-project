from pydantic import BaseModel


class TokenOutput(BaseModel):
    token_type: str
    token: str

class AccessTokenData(BaseModel):
    username: str = None
