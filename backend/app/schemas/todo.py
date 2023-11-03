from pydantic import BaseModel, constr


class TodoInput(BaseModel):
    title: constr(max_length=64)
    description: constr(max_length=255)
    
    class Config:
        orm_mode = True


class TodoOutput(BaseModel):
    id: int
    title: str
    description: str
    
    class Config:
        orm_mode = True