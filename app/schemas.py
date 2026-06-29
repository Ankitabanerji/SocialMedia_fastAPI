from datetime import datetime
from pydantic import BaseModel,EmailStr
from typing import Optional


# -------------USER SCHEMAS------------------
class UserBase(BaseModel):
    '''User API base payload schema'''
    email: EmailStr
    password: str

class UserCreate(UserBase):
    '''Create user api payload schema'''

class UserResponse(BaseModel):
    '''User API response schema'''
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        """Pydantic model configuration."""
        from_attributes = True


class UserLogin(BaseModel):
    '''User Login API payload schema'''
    email: EmailStr
    password: str

# --------------POST SCHEMAS-----------------
class PostBase(BaseModel):
    '''Post API base payload schema'''
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    '''Create post api payload schema'''

class PostUpdate(PostBase):
    '''Update post api payload schema'''

class Post(PostBase):
    '''Post API response schema'''
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        """Pydantic model configuration."""
        from_attributes = True

class PostResponse(BaseModel):
    Post: Post
    votes: int

    class Config:
        """Pydantic model configuration."""
        from_attributes = True


class AccessToken(BaseModel):
    '''Login Access Token response schema'''
    access_token: str
    token_type: str
    class Config:
        """Pydantic model configuration."""
        from_attributes = True

class TokenData(BaseModel):
    user_id: Optional[int]=None

class Vote(BaseModel):
    post_id: int
    vote_dir: int