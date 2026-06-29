from fastapi import  HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app import schemas, models, oauth2
from app.database import get_db

vote_router = APIRouter(prefix="/vote", tags=['Vote'])

@vote_router.post("/", status_code=status.HTTP_201_CREATED)
def vote_post(vote:schemas.Vote,
              db: Session=Depends(get_db),
              get_current_user: models.User= Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id:{vote.post_id} does not exist.")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id== vote.post_id,
                                              models.Vote.user_id==get_current_user.id)
    found_vote = vote_query.first()
    if vote.vote_dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"User {get_current_user.id} has already liked "
                    f"post {vote.post_id}"
                ),
            )
        new_vote = models.Vote(user_id=get_current_user.id, post_id= vote.post_id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully removed vote"}
