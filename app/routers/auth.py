from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, status, HTTPException, Depends, Response
from app.schemes.auth import PasswordRecovery, UserEmail
from app.schemes.users import CreateUserScheme
from app.shared.dependencies import db_dependency, user_dependency, bcrypt_context
from app.models.users import UsersModel
from app.shared.dependencies import authenticate_user, create_access_token

router = APIRouter(
    prefix='/account',
    tags=['Auth']
)


@router.post(path='/sign-up', status_code=status.HTTP_201_CREATED, description='Create a new user')
async def create_user(db: db_dependency, user: CreateUserScheme):
    try:
        existing_user = db.query(UsersModel).filter(
            (UsersModel.email == user.email) | (UsersModel.username == user.username)).first()

        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already exists')

        new_user = UsersModel(**user.model_dump())
        db.add(new_user)
        db.commit()

    except HTTPException as e:
        raise e


@router.post(path='/sign-in', status_code=status.HTTP_200_OK, description='User login')
async def login_for_access_token(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User does not exist')
    token_expires = timedelta(60)
    token = create_access_token(username=user.username, user_id=user.id, role=user.role, shelter_id=user.shelter_id,
                                expires_delta=token_expires)
    response.set_cookie(key='access_token', value=token, httponly=True)
    return {'access_token': token, 'token_type': 'bearer'}


@router.get('/logout', status_code=status.HTTP_200_OK)
async def log_out_user(user: user_dependency, response: Response):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Authentication failed')
    response.delete_cookie('access_token')


@router.post('/password-recovery', status_code=status.HTTP_204_NO_CONTENT)
async def update_user_password(db: db_dependency, user_email: UserEmail):
    existing_user = db.query(UsersModel).filter(UsersModel.email == user_email.email).first()

    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User with this email is not found')
    return existing_user


@router.put('/password-recovery')
async def reset_user_password(
        db: db_dependency,
        password_verification: PasswordRecovery,
        existing_user: UsersModel = Depends(update_user_password)
):
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    if password_verification.new_password != password_verification.repeat_password:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Error on password change')

    existing_user.hashed_password = bcrypt_context.hash(password_verification.new_password)
    db.add(existing_user)
    db.commit()
