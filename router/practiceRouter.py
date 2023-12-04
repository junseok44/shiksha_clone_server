from fastapi import APIRouter
from db.database import get_db
from db.model import ProblemSet,User
from sqlalchemy import select

router = APIRouter(
    prefix="/practice",
)


@router.get("/user/{id}")
def get_user(id: int):
    user = None
    with get_db() as db:
        stmt = select(User).where(User.id == id)
        result = db.scalars(stmt)

        for row in result:
            user = row

    if user is None:
        return {
            "result": "No user"
        }
    

    return {
        "result": user
    }


@router.get("/user/create")
def create_user(user_id: str, password: str, username: str):
    return {"user_id": user_id, "password": password, "username": username}
@router.get("/problemSetWithUser")


def practice_relationship():
    with get_db() as db:
        result = []
        stmt = select(ProblemSet)
        rows = db.scalars(stmt).all()        
        for data in rows:
            result.append(data.creator)            
        return {"result": result}


@router.get("/problemSet/list")
def get_problem_list():
    result = []
    with get_db() as db:
        stmt = select(ProblemSet)
        scalars = db.scalars(stmt)
        for row in scalars:
            result.append(row)
    return {"result": result}


@router.get("/problemSet/create")
def create_problem_set():
    with get_db() as db:
        problemSet = ProblemSet(desc="으하하", creator_id=1)
        db.add(problemSet)
        db.commit()
    
        return {"desc": problemSet.desc, "creator_id": problemSet.creator_id}

@router.get("/problemSet/{id}")
def get_problem_set(id: int):
    problem_sets = None
    with get_db() as db:
        stmt = select(ProblemSet).where(ProblemSet.id == id)
        result = db.scalars(stmt)
        for row in result:
            problem_sets = row

    return {
        "problem_sets": problem_sets
    }


