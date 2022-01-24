from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import  posts , users, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host = "localhost",database = 'fastapi',user= "postgres",password = '122354122',cursor_factory=RealDictCursor )
        cursor = conn.cursor()
        print('database connection successful')
        break        
    except Exception as error:
        print("database connection failed.. Trying again ")
        print('error :', error)
        time.sleep(2)

my_post = [{'title':"title of the post 1", 'content': 'content of post 1', 'id' : 1},{"title":"favourite food","content":"I like pizza","id":2}]

def findPost(id):
    for p in my_post:
        if p['id']== id:
            return p

def FindIndex(id):
    for i,p in enumerate(my_post):
        if p['id']==id:
            return i

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")  
async def root():
    return {"Hello World, how are you!!!"}

