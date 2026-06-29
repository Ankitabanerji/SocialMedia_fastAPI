from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, utils, oauth2, schemas
from app.database import get_db

auth_router = APIRouter(tags=['Authentication'])

@auth_router.post("/login", response_model=schemas.AccessToken)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    '''User Login'''
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")

    if not utils.verify_password(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token":access_token, "token_type": "bearer"}
