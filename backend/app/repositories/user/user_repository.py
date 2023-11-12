from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user.user_repository_interface import UserRepositoryInterface
from app.schemas.user import UserInput


class UserRepository(UserRepositoryInterface):    
    
    def __init__(self, db: Session):
        self.db = db
    
    
    def find_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()
    
    
    def create(self, user_input: UserInput) -> User:
        user = User(
            username=user_input.username,
            password=user_input.password
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
