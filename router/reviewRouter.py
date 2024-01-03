from fastapi import APIRouter, HTTPException, Header
from db.database import get_db
from db.model import Review,Menu
from sqlalchemy import select   
from pydantic import BaseModel
from typing import Annotated
from services.jwt import get_user_id_by_token

router = APIRouter(
    prefix="/review", 
)

class TReview(BaseModel):    
    menuId: int
    text: str
    rating: int

@router.get("/menu/{menu_id}")
async def get_menu_review(menu_id: int):
    with get_db() as db:
        df = db.scalars(select(Review).where(Review.menuId == menu_id))
        menu = db.scalar(select(Menu).where(Menu.id == menu_id))
        reviews = []
        reviewAverage = 0
        # review들의 menuId를 가져와야 함.
        if df is None:
            return HTTPException(status_code=400, detail="Invalid Request")

        for review in df:
            reviews.append({
                "id": review.id,    
                "text": review.text,
                "rating": review.rating,
                "writer": review.writer.username
            })
            reviewAverage += review.rating
        
        if len(reviews) != 0:
            reviewAverage /= len(reviews)
   
        return {"reviews": reviews, 
                    "menu": menu.name,
                    "reviewAverage": reviewAverage,
                    "reviewCount": len(reviews),
                    "likes": 12}



@router.post("/menu/{menu_id}")
async def post_menu_review(review: TReview, Authorization: Annotated[str | None, Header()]):
    with get_db() as db:
        try:
            if not Authorization:
                return HTTPException(status_code=401, detail="Invalid Token")
            Authorization = Authorization.split(" ")[1]
            user_id = get_user_id_by_token(Authorization)

            if not user_id:
                return HTTPException(status_code=401, detail="Invalid Token")

            review = Review(menuId=review.menuId, text=review.text, rating=review.rating, writerId=1)
            db.add(review)
            db.commit()

            return {"message": "success"}

        except:
            return HTTPException(status_code=400, detail="Invalid Request")


@router.delete("/menu/{menu_id}")   
async def delete_menu_review(menu_id: int):
    with get_db() as db:
        try:
            db.delete(select(Review).where(Review.menuId == menu_id))
            db.commit()
        except:
            return HTTPException(status_code=400, detail="Invalid Request")

@router.post("/menu/{menu_id}/edit")
async def edit_menu_review(menu_id: int):
    with get_db() as db:
        try:
            db.update(select(Review).where(Review.menuId == menu_id))
            db.commit()
        except:
            return HTTPException(status_code=400, detail="Invalid Request")
        else:
            return {"message": "Hello World"}
