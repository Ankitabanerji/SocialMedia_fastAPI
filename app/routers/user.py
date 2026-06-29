from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session
from app import schemas, models, utils
from app.database import get_db

user_router = APIRouter(prefix="/users", tags=['Users'])

@user_router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    '''Create user'''
    hashed_pass = utils.hash_password(user.password)
    user.password = hashed_pass
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
