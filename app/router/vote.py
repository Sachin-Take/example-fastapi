from fastapi import FastAPI,Response,status,HTTPException,Depends, APIRouter
from .. import database,schemas,models,oauth2 
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags= ['vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,db: Session = Depends(get_db),
         current_user:Session=Depends(oauth2.get_current_user)):
    
    post =  db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post: #it check post is exist or not which is liked by user
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{vote.post_id} not exist")
    
    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id,models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1): #for like or add vote to post
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail= f"user {current_user.id} has already voted on post{vote.post_id}")
        new_vote= models.Votes(post_id= vote.post_id,user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    
    else: #for dislike or delete vote
        if not vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"vote doesnt exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted successfully"}