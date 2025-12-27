from jose import jwt,JWTError
from datetime import datetime,timezone,timedelta
import os
from dotenv import load_dotenv

load_dotenv()

algorithm = os.getenv("ALGORITHM")
expireTime = os.getenv("TOKEN_EXPIRE_TIME_MINUTES")
secretKey = os.getenv("SECRET_KEY")

def createJwtToken(payload: dict):
    to_encode = payload.copy()

    expire = datetime.now(timezone.utc) + timedelta(int(expireTime))

    to_encode.update({"exp":expire})

    encodedJwt = jwt.encode(to_encode,secretKey,algorithm = algorithm)

    return encodedJwt

