from fastapi import APIRouter,Depends,HTTPException
from database import get_db
from sqlalchemy.orm import Session
from schema import CreateUser
from models import Users
from routers.security.hashPass import hash_pass

User = APIRouter(prefix="/user",tags=["Users"])

@User.post("/")
async def create_user(new_user: CreateUser,db: Session = Depends(get_db)):

    user = db.query(Users).filter(Users.user_name==new_user.user_name).first()

    if user:
        raise HTTPException(status_code=409, detail = "User already exists")
    
    user = Users(
        user_name = new_user.user_name,
        email = new_user.email,
        password_hash = hash_pass(new_user.password),
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