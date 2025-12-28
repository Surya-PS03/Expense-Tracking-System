from fastapi import FastAPI,Depends
from routers import Category, User
from database import engine,Base
import models
from database import get_db
from sqlalchemy.orm import Session
from routers import auth
app = FastAPI()

app.include_router(User.User)
app.include_router(Category.Category)
app.include_router(auth.auth)

@app.get("/health")
def check_health(db: Session = Depends(get_db)):
    return {"status":"OKAY"}
