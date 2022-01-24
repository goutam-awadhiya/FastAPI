from .. import models, schema
from typing import List 
from fastapi import HTTPException, Depends,status, APIRouter, Response
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)

#using ORM
@router.get("/",response_model=List[schema.Post])
def get_posts(db : Session=Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# using ORM 
@router.get("/{id}",response_model=schema.Post)
def getById(id, db : Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"item with {id} not found")
    return post

#implement using ORM
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def createpost(post: schema.PostCreate,db: Session=Depends(get_db)):
    new_post = models.Post(**post.dict())
    #new_post = models.Post(title=post.title,content=post.content,published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    
#using ORM
@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id, db:Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# using ORM
@router.put("/{id}",response_model=schema.Post)
def updateRecord(id,updated_post : schema.PostCreate, db:Session= Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} is not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()






    







'''
#using the conn object
@app.get("/posts")
def get_posts():
    cursor.execute("""select * from posts""")
    posts = cursor.fetchall()
    print(posts)
    return {posts}

# using the conn object
@app.get('/posts/{id}')
def getById(id:int):
    cursor.execute("""select * from posts where id = %s""",(str(id)))
    posts = cursor.fetchall()
    if len(posts)==0:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return {posts}

# implemented using conn object
@app.post('/posts',status_code=status.HTTP_201_CREATED)
def createPosts(post:schema.PostCreate):
    cursor.execute("""insert into posts(title,content,published) values(%s,%s,%s) returning *""",(post.title,post.content,post.published))
    new_post = cursor.fetchall()
    conn.commit()
    return { 'post': new_post}

# same as above implemented using payload : dict = Body(...)
@app.post("/posts")
def create_posts(payload : dict = Body(...) ):
    print(payload)
    string = 'title :'+payload['title']+'content :'+payload['content']
    return {'new post': string}

#implemented using conn object
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id:int):
    cursor.execute("""delete from posts where id = %s returning *""",(str(id),))
    post = cursor.fetchall()
    if len(post)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='post not found')
    conn.commit()
    return {'del_post':post,'result':'post is deleted'}

#implemented using conn 
@app.put("/posts/{id}")
def UpdateRecord(id:int,post : schema.PostCreate):
    cursor.execute("""select * from posts where id = %s""",(str(id)))
    posts = cursor.fetchall()
    if len(posts)==0:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    else:
        cursor.execute("""update posts set title = %s, content = %s, published = %s where id = %s returning *""",(post.title,post.content,post.published,id))
        post = cursor.fetchall()
    conn.commit()
    return {'old':posts,'new':post}

# same as above implemented using payload : dict = Body(...)
@app.put("/posts/{id}")
def updateRecord(id:int,payload : dict=Body(...)):
    index = FindIndex(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Record with id = {id} not found')
    print(payload)
    for key in payload.keys():
        my_post[index][key]=payload[key]
    print(my_post)
    return {"message":"updated post"}
'''