from typing import Union
from db.model import User, ProblemSet
from db.database import get_db
from fastapi import FastAPI
from sqlalchemy import select
from router.practiceRouter import router as practice_router
from router.authRouter import router as auth_router 


app = FastAPI()

# app.include_router(practice_router)
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}






