from database import setting

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get():
    return {'name': 'Mike'}

@router.post("/create")
def create():
    session = setting.get_db()
