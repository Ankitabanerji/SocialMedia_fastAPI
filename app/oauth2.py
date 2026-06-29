from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
from app import schemas, models
from app.database import get_db
from app.config import settings

SECRET_KEY = settings.secret_key_jwt
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    '''Create Access Token'''
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    '''Verify Access Token'''
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        userid:int = payload.get("user_id")

        if not userid:
            raise credentials_exception
        token_data = schemas.TokenData(user_id=userid)

    except InvalidTokenError as exc:
        raise credentials_exception from exc

    return token_data
    
def get_current_user(token: str= Depends(oauth2_scheme), db: Session = Depends(get_db)):
    '''Get Current User'''
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.user_id).first()
    return user
