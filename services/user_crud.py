from db.model import User
from sqlalchemy import select
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(user_id: str, password: str, username: str, db):
    user = User(user_id=user_id, password=
            pwd_context.hash(password)
                , username=username)
    db.add(user)
    db.commit()
    return user

def get_user_by_user_id(user_id: str,db):
    user = db.scalar(select(User).where(User.user_id == user_id))
    print(user)
    return user

def check_password(user: User, password: str):  
    return pwd_context.verify(password, user.password)

def update_user(user_id: str, password: str, username: str):
    pass

def delete_user(user_id: str):
    pass
