from fastapi import APIRouter,Depends,HTTPException
from database import get_db
from sqlalchemy.orm import Session
from schema import CreateUser
from models import Users
createUser = APIRouter(prefix="/user",tags=["Users"])

@createUser.post("/")
async def create_user(new_user: CreateUser,db: Session = Depends(get_db)):

    user = db.query(Users).first()

    if user:
        raise HTTPException(status_code=409, detail = "User already exists")
    
    user = Users(
        user_name = new_user.user_name,
        email = new_user.email,
        password_hash = new_user.password_hash,
        dob = new_user.dob,
        total_earning = new_user.total_earning
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.user_id,
        "user_name": user.user_name,
        "email": user.email
    }