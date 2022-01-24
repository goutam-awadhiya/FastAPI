from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, schema, models,utils

router = APIRouter(tags = ["Auth"])

@router.post("/login")
def login(user_credentials: schema.UserLogin, db : Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email==user_credentials.email).first()
    if not user or not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid credentials")

    #implement token

    #generate token

    return {"message":"token generated"}






