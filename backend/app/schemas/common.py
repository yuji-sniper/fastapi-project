from pydantic import BaseModel


class Ok(BaseModel):
    message: str
