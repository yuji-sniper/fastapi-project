from pydantic import BaseModel


class TokenOutput(BaseModel):
    token: str = None
