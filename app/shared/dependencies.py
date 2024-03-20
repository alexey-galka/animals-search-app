from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
from fastapi import Depends, status, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from app.database import SessionLocal
from typing import Annotated, Optional
from app.models.users import UsersModel


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='account/sign-in')


def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(UsersModel).filter(UsersModel.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    if not bcrypt_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Password is wrong')
    return user


def create_access_token(username: str, user_id: int, role: str, shelter_id: int, expires_delta: Optional[timedelta] = None):
    encode = {'sub': username, 'id': user_id, 'role': role, 'shelter_id': shelter_id}
    if expires_delta:
        expires = datetime.now(timezone.utc) + expires_delta
    else:
        expires = datetime.now(timezone.utc) + timedelta(minutes=15)
    encode.update({'exp': expires})
    return jwt.encode(claims=encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        shelter_id: int = payload.get('shelter_id')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        return {'username': username, 'id': user_id, 'role': user_role, 'shelter_id': shelter_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')


user_dependency = Annotated[str, Depends(get_current_user)]
