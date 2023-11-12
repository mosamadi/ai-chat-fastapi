from typing import Annotated
from fastapi import APIRouter,Depends
from fastapi import status,HTTPException
from fastapi.security import  OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.database import get_db_session
from .schemas import UserCreation,AccessTokenResponse,UserLogin,BaseUser
from .services import create_access_token,get_user_by_email,verify_password,create_user
 


router = APIRouter()


@router.post('/register',status_code=status.HTTP_201_CREATED)
def user_registration(user:UserCreation,session: Session = Depends(get_db_session)) -> AccessTokenResponse:
    existing_user = get_user_by_email(user.email,session)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    create_user(session,user)

    access_token = create_access_token(data={"sub": user.email})

    return AccessTokenResponse(**{"access_token": access_token,},**user.model_dump())



@router.post('/login',status_code=status.HTTP_200_OK)
def user_login(user:UserLogin,session: Session = Depends(get_db_session)):
    db_user = get_user_by_email(user.email, session )
    if not db_user:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User dosen't exist!")
    if not verify_password( user.password, db_user.password):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Password dosen't match!")
    access_token = create_access_token(data={"sub": user.email})
    return AccessTokenResponse(**{"access_token": access_token},**db_user.__dict__)

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],session: Session = Depends(get_db_session)):
    db_user = get_user_by_email(form_data.username, session )
    if not db_user:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User dosen't exist!")
    if not verify_password( form_data.password, db_user.password):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Password dosen't match!")
    return {"access_token": create_access_token(data={"sub": db_user.email}), "token_type": "bearer"}

