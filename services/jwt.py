from jose import JWTError, jwt
import os
from .user_crud import get_user_by_user_id
from db.database import get_db

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRE_MINUTES = os.getenv("JWT_EXPIRE_MINUTES")

async def get_user_id_by_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = payload['user_id']
        with get_db() as db:
            user_query = get_user_by_user_id(user_id, db)
            if not user_query:
                return None
        return payload['user_id']

    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception as e:
        print(e)
        return None