from fastapi import Depends,APIRouter,HTTPException,status
from sqlalchemy.orm import Session
from database import get_db
from models import Categories,Users
from schema import CreateCategory
from routers.security.auth import get_current_user

Category = APIRouter(prefix = "/category",tags = ["Categories"])


@Category.post("/create_category")
async def create_category(category: CreateCategory,db: Session = Depends(get_db),current_user: Users = Depends(get_current_user)):
    
    user_category = db.query(Categories).filter(Categories.user_id == current_user.user_id, Categories.category_name == category.cat_name).first()

    if user_category:
        raise HTTPException(status_code = 409, detail ="Category already exists")
    
    cat = Categories(user_id = current_user.user_id,
                     category_name = category.cat_name)
    
    db.add(cat)
    db.commit()
    db.refresh(cat)

    return {"user_id":current_user.user_id,"category_name":category.cat_name}
        
@Category.get("/get_categories")
async def get_categories(db: Session = Depends(get_db),curr_user: Users = Depends(get_current_user)):

    user_id = curr_user.user_id

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid Request")
    
    allCategories = db.query(Categories).filter(Categories.user_id==curr_user.user_id).all()

    if allCategories is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "No category created by the user")
    
    return allCategories

