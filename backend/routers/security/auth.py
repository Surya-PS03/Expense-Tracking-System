from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from database import get_db
from models import Users
from jose import jwt,JWTError,ExpiredSignatureError
import os
from dotenv import load_dotenv

load_dotenv()
algorithm = os.getenv("ALGORITHM")
secret_key = os.getenv("SECRET_KEY")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):

    try:
        payload = jwt.decode(token, secret_key, algorithms = [algorithm])
        user_id = payload.get('sub')

        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid Token")
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = "Token has expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid Token")
    
    user = db.query(Users).filter(Users.user_id == int(user_id)).first()

    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "User not found")
    
    return user
    
