from fastapi import FastAPI,Depends
from database import engine,Base
import models
from database import get_db
from sqlalchemy.orm import Session
from routers import createCategory,createUser,auth
app = FastAPI()

app.include_router(createUser.createUser)
app.include_router(createCategory.createCategory)
app.include_router(auth.auth)

@app.get("/health")
def check_health(db: Session = Depends(get_db)):
    return {"status":"OKAY"}
