from fastapi import FastAPI,Response,status,HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas,utils

router = APIRouter(
    prefix= "/users",
    tags=["Users"]
)

#CREATE AND STORE USER
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session= Depends(get_db)):
    new_id = models.User(**user.model_dump())
    user_id = db.query(models.User).filter(models.User.id == new_id.id).first()
    user_email = db.query(models.User).filter(models.User.email == new_id.email).first()
    if  not user_id: 
        if not user_email:
            hashed_password= utils.hash(user.password)
            user.password = hashed_password
            new_user = models.User(**user.model_dump())
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        else:
            raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,
                            detail=f"user with Email:{user.email} alredy exist")
    else:       
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,
                            detail=f"user with id:{user.id} alredy exist")
#get user info by id
@router.get("/{id}",response_model= schemas.UserOut)
def get_user(id: int, db: Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id:{id} is not found")

    return user 

