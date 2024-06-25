#from itertools import count
from fastapi import FastAPI,Response,status,HTTPException,Depends, APIRouter
import json
from sqlalchemy import func
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, oauth2, schemas
from typing import Optional, List

router = APIRouter(
    prefix= "/posts",
    tags=["posts"]
)

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),
              limit: int=5,skip : int = 0,search: Optional[str]=""):
    #cursor.execute("""SELECT * FROM posts  """)
    #posts= cursor.fetchall() 
    #  it returns all post of loged in user
   # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
    #limit tells about how many posts to be display at one time
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(limit)
    posts = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).outerjoin(
        models.Votes,models.Votes.post_id == models.Post.id).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #print(results)
    return posts

    """posts_data = []
    for post, vote_count in results:
        post_dict = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
             "published": post.published,
             "created_at": post.created_at,                
             "owner_id": post.owner_id,
             "owner":    post.owner,# Adjust based on your actual attribute names
             "votes": vote_count
        }
    posts_data.append(post_dict)

# Serialize posts_data to JSON
    posts_json = json.dumps(posts_data, default=str)  # default=str to handle datetime objects if needed

# Print or use the JSON data as needed
    #print(posts_json)"""

   
#create post or insert data in database
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session= Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute(f"INSERT INTO posts (title,content,published) 
    #                                    VALUES({post.title},{post.content},{post.published})")
    #cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING *""",
                 #  (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    #bcz of this line approach we need to type all field,so 
    #new_post = models.Post(title=post.title,content=post.content,published=post.published)
    print(current_user.email)
    new_post = models.Post(owner_id= current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

"""@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0,1000)
    my_post.append(post_dict)
    return {"data": my_post}
this method create post in my_post variable
    """

#retrive post from db by post id
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: str,db: Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    #post= cursor.fetchone()
    #print(post)
    #post = find_post(id)
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).outerjoin(
                models.Votes,models.Votes.post_id == models.Post.id).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"post with {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message':f"post with {id} was not found"}
    
   # if post.owner_id != current_user.id :
       # raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                           # detail=f"not authorized to perform this operation")"""
    
    
    return post

@router.delete("/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    delete_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = delete_query.first()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} is not found")

    if deleted_post.owner_id != current_user.id :
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail=f"not authorized to perform this operation")
    delete_query.delete(synchronize_session=False)
    
    db.commit()
    #my_post.pop(index)
    #return {"message":"Post successfully deleted"}
    return Response(status_code= status.HTTP_204_NO_CONTENT)
    
 #update operation
@router.put("/{id}", response_model=schemas.Post)
def post_update(id: int,updated_post: schemas.PostCreate,db: Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} is not found")

    if post.owner_id != current_user.id :
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail=f"not authorized to perform this operation")
    
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first() 
