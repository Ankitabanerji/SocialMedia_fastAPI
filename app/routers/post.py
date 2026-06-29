from typing import List, Optional
from fastapi import Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import schemas, models, oauth2
from app.database import get_db

post_router = APIRouter(prefix="/posts", tags=['Posts'])

@post_router.get("/",response_model=List[schemas.PostResponse])
def get_posts(db: Session=Depends(get_db),
              get_current_user: models.User= Depends(oauth2.get_current_user),
              limit: int= 10, skip: int=0, search: Optional[str]=""
              ):
    '''Get all the posts'''
    results = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes")
        )
        .join(
            models.Vote,
            models.Post.id == models.Vote.post_id,
            isouter=True
        )
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return results

@post_router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def creat_posts(post: schemas.PostCreate, db: Session=Depends(get_db),
                get_current_user: int= Depends(oauth2.get_current_user)):
    '''Create post'''
    new_post = models.Post(owner_id=get_current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@post_router.get("/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, db: Session=Depends(get_db),
             get_current_user: int= Depends(oauth2.get_current_user)):
    '''Get a post with id'''
    post = db.query(models.Post).filter(models.Post.id==post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with Id: {post_id} not found")
    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not Authorized")
    return post

@post_router.delete("/{post_id}", response_model=schemas.Post)
def delete_post(post_id: int, db: Session=Depends(get_db),
                get_current_user: int= Depends(oauth2.get_current_user)):
    '''Delete a post with id'''
    post = db.query(models.Post).filter(models.Post.id==post_id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with Id: {post_id} not found")
    if post.first().owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authorized to perform delete operation")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@post_router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, updated_post:schemas.PostUpdate, db: Session=Depends(get_db),
                get_current_user: int= Depends(oauth2.get_current_user)):
    '''Update a post with id'''
    post_query = db.query(models.Post).filter(models.Post.id==post_id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with Id: {post_id} not found")

    if post_query.first().owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authorized to perform update operation")        
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()
