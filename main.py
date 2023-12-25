from db.model import User
from db.database import get_db
from fastapi import FastAPI
from sqlalchemy import select
from router.authRouter import router as auth_router 
from router.cafeRouter import router as cafe_router
from router.menuRouter import router as menu_router
from router.reviewRouter import router as review_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(cafe_router)
app.include_router(menu_router)
app.include_router(review_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}






