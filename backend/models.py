from database import Base
from sqlalchemy import Column,Integer,DateTime,String,Date,Float,CheckConstraint,Boolean,ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR
from datetime import datetime,timezone

class Users(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer,primary_key= True)
    user_name = Column(String(50),nullable = False)

    ##used it because of case issue in mail, standard used only lower case
    email = Column(VARCHAR(255, collation ="utf8mb4_0900_ai_ci"), unique = True, nullable=False)
    dob = Column(Date,nullable = False)

    # total_earning=0 will cause negative savings issue so using null is viable
    total_earning = Column(Float,CheckConstraint("total_earning>=0",name = "check_earning_positive"),nullable = True) 

class Expenses(Base):

    __tablename__ = 'Expenses'

    exp_id = Column(Integer,primary_key = True)
    user_id = Column(Integer, ForeignKey("Users.user_id"),nullable = False)

    ##Check contraints for irregular values 
    price = Column(Float,CheckConstraint("price>0",name = "check_amount_positive"),nullable = False)
    quantity = Column(Integer,CheckConstraint("quantity>0",name = "check_quantity_positive"),nullable = False)
    
    ## lambda function for whenever a new entry is done current UTC time stamp is used instead of when the model was created at
    created_at = Column(DateTime(timezone=True),
                        default = lambda: datetime.now(timezone.utc),
                        nullable=False)

    description = Column(String(450),nullable = True)

class Categories(Base):

    __tablename__ = 'Categories'

    cat_id = Column(Integer,primary_key = True)
    user_id = Column(Integer,ForeignKey("Users.user_id"),nullable = False)
    category_name = Column(VARCHAR(50, collation = "utf8mb4_0900_ai_ci"),nullable=False)
    is_active = Column(Boolean,nullable = False, default = True)
    created_at = Column(DateTime(timezone=True),
                        default = lambda: datetime.now(timezone.utc),
                        nullable = False)