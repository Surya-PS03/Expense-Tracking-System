from fastapi import FastAPI,Depends
from database import engine,Base
import models
from database import get_db
from sqlalchemy.orm import Session
from routers.createUser import createUser
app = FastAPI()

app.include_router(createUser)

@app.get("/health")
def check_health(db: Session = Depends(get_db)):
    return {"status":"OKAY"}
