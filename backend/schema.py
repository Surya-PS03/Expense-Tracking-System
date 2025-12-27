from pydantic import BaseModel,EmailStr,Field
from datetime import date
from decimal import Decimal
from typing import Annotated

Money = Annotated[Decimal, Field(max_digits=10,decimal_places=2,ge=Decimal("0.00"))]
class CreateUser(BaseModel):
    user_name: str
    email: EmailStr
    password: str
    dob: date
    total_earning: Money

class CreateCategory(BaseModel):
    cat_name: str

#auth
class LoginRequest(BaseModel):
    user_name: str
    password: str

class TokenRequest(BaseModel):
    access_token: str
    token_type: str = 'bearer' 