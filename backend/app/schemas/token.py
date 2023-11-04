from pydantic import BaseModel


class AccessTokenData(BaseModel):
    username: str = None
