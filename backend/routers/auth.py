from fastapi import Depends,APIRouter,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from schema import LoginRequest
from database import get_db
from sqlalchemy.orm import Session
from models import Users
from routers.security.hashPass import verify_pass
from routers.security.jwtAuth import createJwtToken
from schema import LoginRequest

auth = APIRouter(prefix = "/auth",tags = ['auth'])

@auth.post('/login')
async def login(payload: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):

    user = db.query(Users).filter(Users.user_name==payload.username).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Not Authorized")
    
    if not verify_pass(payload.password,user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = "Invalid Credentials")
    
    access_token = createJwtToken(payload = {'sub':str(user.user_id)})
    return {'access_token':access_token}
