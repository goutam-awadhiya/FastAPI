from typing import List 
from fastapi import HTTPException, Depends, status, Response, APIRouter
from ..database import get_db
from .. import models, schema, utils
from sqlalchemy.orm import Session


router = APIRouter(
    prefix = "/users",
    tags =  ["Users"]
)


@router.get('/',response_model=List[schema.UserOut])
def GetUsers(db : Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user


@router.get('/{id}', response_model=schema.UserOut)
def GetUserById(id, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user with {id} not found')
    return user

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def createuser(user : schema.UserCreate,db: Session = Depends(get_db)):
    hashed_password = utils.Hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def DeleteUser(id,db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id)
    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with {id} not found')
    user.delete(synchronize_session = False)
    db.commit()
    return (Response(status_code=status.HTTP_204_NO_CONTENT))

@router.put('/{id}',response_model=schema.UserOut)
def UpdateUser(id,updated_user : schema.UserCreate, db : Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id==id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} not found")
    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()

