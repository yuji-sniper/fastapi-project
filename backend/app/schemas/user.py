from pydantic import BaseModel, constr, validator
import re


class UserInput(BaseModel):
    username: constr(max_length=64)
    password: constr(max_length=64, min_length=8)
    
    @validator('password')
    def password_complexity(cls, v):
        pattern = re.compile(r'^(?=.*[a-z])(?=.*\d)[a-zA-Z\d]{8,}$')
        if not pattern.match(v):
            raise ValueError('Password must contain at least one lowercase letter and one number')
        return v
    
    class Config:
        orm_mode = True


class UserOutput(BaseModel):
    id: int
    username: constr(max_length=64)
    
    class Config:
        orm_mode = True
