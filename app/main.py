from fastapi import FastAPI
from . import models 
from .router import user, post,auth,vote
from  .database import engine
from .confg import settings
from fastapi.middleware.cors import CORSMiddleware

#create table in database
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origin=origins,
    allow_credentials=[],
    allow_methods=["*"],
    allow_headers=["*"]

)

 #conneting to postgres database   
     

"""my_post = [{"title":"post 1","content":"content of post1","id":1},
           {"title":"post 2","content":"content of post2","id":2}]

@app.get("/")
async def root():
    #print("Hello Python")
    return {"message": "Welcome to my APi"}
"""
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

"""
def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p
        
#find  post index to delete it
def find_post_index(id):
    for i,p in enumerate(my_post):
        if p['id']== id:
            return i 

@app.get("/posts/latest")
def get_latest_post():
    post = my_post[len(my_post)-1]
    return post
    
"""
