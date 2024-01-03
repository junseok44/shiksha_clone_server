from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from services.user_crud import create_user, get_user_by_user_id, update_user, delete_user, check_password
from db.database import get_db  
from dotenv import load_dotenv
import os
from datetime import timedelta
from jose import JWTError, jwt
from datetime import datetime

load_dotenv(verbose=True)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRE_MINUTES = os.getenv("JWT_EXPIRE_MINUTES")


router = APIRouter(
    prefix="/user",
)

class AuthForm(BaseModel):
    user_id: str
    password: str

    @validator("user_id")
    def user_id_validator(cls, v):
        if len(v) < 4:
            raise HTTPException(status_code=422, detail="user_id must be longer than 4")
        return v
    
    @validator("user_id", "password")
    def is_empty(cls, v):
        if len(v) == 0:
            raise HTTPException(status_code=422, detail="user_id, password, username must not be empty")
        return v
    
    @validator("password")
    def password_validator(cls, v):
        if len(v) < 8:
            raise HTTPException(status_code=422, detail="password must be longer than 8")

        if not any([c.isupper() for c in v]):
            raise HTTPException(status_code=422, detail="password must contain at least one uppercase letter")
        
        if not any([c.isdigit() for c in v]):
            raise HTTPException(status_code=422, detail="password must contain at least one number")
        
        if not any([c.isalpha() for c in v]):
            raise HTTPException(status_code=422, detail="password must contain at least one alphabet")
        return v
    

class LoginForm(BaseModel):
    user_id: str
    password: str

    @validator("user_id")
    def user_id_validator(cls, v):
        if len(v) < 4:
            raise HTTPException(status_code=422, detail="user_id must be longer than 4")
        return v
    
    @validator("user_id", "password")
    def is_empty(cls, v):
        if len(v) == 0:
            raise HTTPException(status_code=422, detail="user_id, password must not be empty")
        return v
    
    @validator("password")
    def password_validator(cls, v):
        if len(v) < 8:
            raise HTTPException(status_code=422, detail="password must be longer than 8")

        if not any([c.isupper() for c in v]):
            raise HTTPException(status_code=422, detail="password must contain at least one uppercase letter")
        
        if not any([c.isdigit() for c in v]):
            raise HTTPException(status_code=422, detail="password must contain at least one number")
        
        if not any([c.isalpha() for c in v]):
            raise HTTPException(status_code=422, detail="password must contain at least one alphabet")
        return v


class JWTToken(BaseModel):
    access_token: str
    token_type: str


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/signup")
async def signup(userForm: AuthForm):
    with get_db() as db:
        user = get_user_by_user_id(userForm.user_id, db)
        if user:
            raise HTTPException(status_code=409, detail="user_id already exists")
        
        newUser = create_user(userForm.user_id, userForm.password, None, db)
        return {
            "result" : "success",
            "user_id" : newUser.user_id,
        }
    
@router.post("/login")
async def login(loginForm: LoginForm):
    with get_db() as db:
        user = get_user_by_user_id(loginForm.user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="user_id not found")
        
        if not check_password(user, loginForm.password):
            raise HTTPException(status_code=401, detail="password incorrect")

        access_token_expires = timedelta(minutes=int(JWT_EXPIRE_MINUTES))
        access_token = jwt.encode({
            'exp': datetime.utcnow().timestamp() + access_token_expires.total_seconds(),
            'user_id': user.user_id,
        },JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        
        refresh_token_expires = timedelta(days=30)
        refresh_token = jwt.encode({
            'exp': datetime.utcnow().timestamp() + refresh_token_expires.total_seconds(),
            'user_id': user.user_id,
        },JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


        return {
            "result" : "success",
            "user_id" : user.user_id,
            "username" : user.username,
            "access_token" : access_token,
            "refresh_token" : refresh_token,
        }


# 미들웨어로 옮겨줄것.
@router.post("/validate")
async def validate(token: str,user_id: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        if payload['user_id'] != user_id:
            raise HTTPException(status_code=401, detail="user_id not match")
    except JWTError:
        raise HTTPException(status_code=401, detail="token invalid")
    
    return {
        "result" : "success"
    }

@router.post("/refresh")
async def refresh(req: RefreshRequest):
    try:
        refresh_token = req.refresh_token
        print(refresh_token)
        payload = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

    except JWTError as e:
        print(e)
        raise HTTPException(status_code=401, detail="token invalid")
    
    user_id = payload['user_id']
    print(user_id)
    with get_db() as db:
        user_query = get_user_by_user_id(user_id, db)
        if not user_query:
            raise HTTPException(status_code=404, detail="user_id not found")
        
        access_token_expires = timedelta(minutes=int(JWT_EXPIRE_MINUTES))
        access_token = jwt.encode({
            'exp': datetime.utcnow().timestamp() + access_token_expires.total_seconds(),
            'user_id': user_id,
        },JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        
        return {
            "result" : "success",
            "access_token" : access_token,
        }



@router.get("/logout")
async def logout():
    return {
        "result" : "success"
    }



