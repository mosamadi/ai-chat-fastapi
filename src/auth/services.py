import os
from datetime import timedelta, datetime
import jwt
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from fastapi import status,Depends
from sqlalchemy.orm import Session
from . import schemas,models
from src.database import get_db_session
from src.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


SECRET_KEY = settings.IFS_JWT_SECRET_KEY
ALGORITHM = settings.IFS_JWT_ALGORITHM
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(email: str,session: Session ) -> models.UserModel:
    return  session.query(models.UserModel).filter_by(email = email).first()


def create_user(db: Session, user: schemas.UserCreation):
    data  = user.model_dump()
    data.update({"password":get_hashed_password(user.password)})
    db_user = models.UserModel( **data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_auth_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db_session)) -> models.UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except PyJWTError:
        raise credentials_exception
    user = get_user_by_email( token_data.email,db)
    if user is None:
        raise credentials_exception
    return user


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)
