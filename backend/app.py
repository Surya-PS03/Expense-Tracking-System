from fastapi import FastAPI
from database import engine,Base
import models
app = FastAPI()
Base.metadata.create_all(bind = engine)

@app.get("/health")
async def check_health():
    return {"health_status":"Good"}