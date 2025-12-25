from database import Base
from sqlalchemy import Column,Integer,DateTime,String,Date,CheckConstraint,Boolean,ForeignKey,Numeric,UniqueConstraint
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from datetime import datetime,timezone

class Users(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer,primary_key= True)
    user_name = Column(String(50),nullable = False)

    ##used it because of case issue in mail, standard used only lower case
    email = Column(VARCHAR(255, collation ="utf8mb4_0900_ai_ci"), unique = True, nullable=False)
    dob = Column(Date,nullable = False)

    # total_earning=0 will cause negative savings issue so using null is viable
    total_earning = Column(Numeric(10,2),CheckConstraint("total_earning>=0",name = "check_earning_positive"),nullable = True) 

    #adding password_hash
    password_hash = Column(String(255),nullable = False)
    # used cascade to remove dangling refrences to ORM object like expenses when a user is deleted and passive_delete when FK has ondelete="Cascade" for efficiency
    expenses = relationship("Expenses",back_populates = "user",cascade= "all, delete-orphan",passive_deletes=True)
    categories = relationship("Categories",back_populates="user",cascade="all, delete-orphan",passive_deletes = True)
class Expenses(Base):

    __tablename__ = 'Expenses'

    exp_id = Column(Integer,primary_key = True)
    #here ondelete=CASCADE mean to delete Expenses corresponding to the user_id 
    user_id = Column(Integer, ForeignKey("Users.user_id",ondelete="CASCADE"),nullable = False,index = True)

    ##Check contraints for irregular values 
    price = Column(Numeric(10,2),CheckConstraint("price>0",name = "check_amount_positive"),nullable = False)
    quantity = Column(Integer,CheckConstraint("quantity>0",name = "check_quantity_positive"),nullable = False)
    
    ## lambda function for whenever a new entry is done current UTC time stamp is used instead of when the model was created at
    created_at = Column(DateTime(timezone=True),
                        default = lambda: datetime.now(timezone.utc),
                        nullable=False)

    #Indexing Forign Key because they aren't automatically indexed and will be used for faster access in future
    #ondelete= CASCADE here to since expenses depend on category
    cat_id = Column(Integer, ForeignKey("Categories.cat_id",ondelete='CASCADE'),nullable = False,index = True) 
    description = Column(String(450),nullable = True)

    user = relationship("Users",back_populates="expenses")
    category = relationship("Categories",back_populates="expenses")

class Categories(Base):

    __tablename__ = 'Categories'

    cat_id = Column(Integer,primary_key = True)
    user_id = Column(Integer,ForeignKey("Users.user_id",ondelete='CASCADE'),nullable = False,index = True)
    category_name = Column(VARCHAR(50, collation = "utf8mb4_0900_ai_ci"),nullable=False)
    is_active = Column(Boolean,nullable = False, default = True)
    created_at = Column(DateTime(timezone=True),
                        default = lambda: datetime.now(timezone.utc),
                        nullable = False)
    
    user = relationship("Users",back_populates = "categories")
    expenses = relationship("Expenses",back_populates="category")

    __table_args__ =(UniqueConstraint("user_id","category_name",name = "uq_user_category"),)