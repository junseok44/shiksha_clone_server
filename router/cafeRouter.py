from fastapi import APIRouter
from sqlalchemy import select
from db.database import get_db
from db.model import Cafe
router = APIRouter(
    prefix="/cafe", 
)

@router.get("/info/{cafeId}")
async def get_cafe_info(cafeId:int):
    with get_db() as db:
        df = db.scalar(select(Cafe).where(Cafe.id == cafeId))
        if df is None:
            return {"message": "Invalid Request"}
        else:
            return {"result": df.__dict__}
