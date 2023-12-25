from fastapi import APIRouter, HTTPException
from datetime import date
from sqlalchemy import select
from db.database import get_db
from db.model import CafeWithMenu, TimeEnum, Menu
from pydantic import BaseModel

router = APIRouter(
    prefix="/menu", 
)   

class TCafeWithMenu(BaseModel):
    cafeId: int
    menuId: int
    atDate: date
    atTime: TimeEnum

class TCafeWithMenuEdit(TCafeWithMenu):
    id: int

class TMenu(BaseModel):
    name: str
    price: int

class TMenuEdit(TMenu):
    id: int


@router.get("/cafeWithMenu/{id}")
async def get_cafe_with_menu(id: int):
    with get_db() as db:
        df = db.scalar(select(CafeWithMenu).where(CafeWithMenu.id == id))
        if df is None:
            return HTTPException(status_code=400, detail="Invalid Request")
        else:
            return {"result": df.__dict__}

@router.get("/weekly/{date}")
async def get_cafe_with_menu_weekly(date: date):
    with get_db() as db:
        try:
            df = db.scalars(select(CafeWithMenu).where(CafeWithMenu.atDate == date))
            result = []
            # menu에 해당하는 모든 review들을 긁어서, 그 raiting의 평균을 내야함.
            for cafeWithMenu in df:
                result.append({
                    **cafeWithMenu.__dict__,
                    "menu": {
                        **cafeWithMenu.menu.__dict__,
                        "raiting": 4.0 
                    },
                    "cafe": {
                        "name": cafeWithMenu.cafe.name,
                    }
                })
            return {"result": result}
        except Exception as e:
            print(e)
            return HTTPException(status_code=400, detail="Invalid Request")

@router.post('/weekly')
async def create_cafe_with_menu(cafeWithMenu: TCafeWithMenu):
    with get_db as db:
        try:
            cafeWithMenu = CafeWithMenu(**cafeWithMenu.model_dump())
            db.add(cafeWithMenu)
            db.commit()
        except:
            db.rollback()
            return HTTPException(status_code=400, detail="Invalid Request")
    return {"message": "success"}

# 근데 edit할때 모든 데이터를 다 받아야 하는건가?
@router.post('/weekly/edit')
async def edit_cafe_with_menu(cafeWithMenu: TCafeWithMenuEdit):
    with get_db as db:
        cm = db.scalar(select(CafeWithMenu).where(CafeWithMenu.id == cafeWithMenu.id))
        if cm is None:
            HTTPException(status_code=400, detail="Invalid Request")
        else:
            cm.cafeId = cafeWithMenu.cafeId
            cm.menuId = cafeWithMenu.menuId
            cm.atDate = cafeWithMenu.atDate
            cm.atTime = cafeWithMenu.atTime
            db.commit()
    return {"message": "success"}


@router.delete('/weekly')
async def delete_cafe_with_menu(id: int):
    with get_db as db:
        db.delete(CafeWithMenu)
        db.commit()
    return {"message": "Hello World"}

# 관리자 페이지에서 테이블을 추가하기 위함.
@router.post("/list")
async def get_menu_list():
    with get_db as db:
        df = db.scalars(select(Menu))
        result = []
        for menu in df:
            result.append({
                **menu.__dict__,
            })
    return {"message": "Hello World"}

# 관리자 페이지에서 메뉴를 수정하기 위함.
@router.post("/edit")
async def edit_menu(id:int):
    with get_db as db:
        menu = db.scalar(select(Menu).where(Menu.id == id))
        if menu is None:
            return HTTPException(status_code=400, detail="Invalid Request")
        else:
            db.commit()
    return {"message": "Hello World"}




