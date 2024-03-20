from fastapi import APIRouter, HTTPException, Response, Path
from starlette import status

from app.models.animals import LostAnimalsModel
from app.models.shelters import SheltersModel
from app.models.users import UsersModel
from app.schemes.settings import PasswordReset
from app.schemes.users import CreateUserScheme
from app.shared.dependencies import user_dependency, db_dependency, bcrypt_context

router = APIRouter(
    prefix='/settings',
    tags=['Settings']
)


@router.put('/security/password-reset', status_code=status.HTTP_202_ACCEPTED, description='Change user password')
async def reset_user_password(
        user: user_dependency,
        db: db_dependency,
        user_verification: PasswordReset
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Authentication failed')

    user_model = db.query(UsersModel).filter(UsersModel.id == user['id']).first()
    if user_model or user['role'] == 'admin':
        if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Error on password change')

        user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
        db.add(user_model)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No permissions')


@router.put('/main/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_profile(
        user: user_dependency,
        db: db_dependency,
        owner: CreateUserScheme,
        user_id: int
):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication is failed')

    existing_owner = db.query(UsersModel).filter(UsersModel.id == user_id).first()

    if existing_owner is None or existing_owner['role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No permissions')

    existing_owner.email = owner.email
    existing_owner.country = owner.country
    existing_owner.city = owner.city
    existing_owner.first_name = owner.first_name
    existing_owner.last_name = owner.last_name

    db.add(existing_owner)
    db.commit()


@router.delete('/main/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
        user: user_dependency,
        db: db_dependency,
        response: Response,
        user_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication is failed')

    if user_id:
        animal_model = db.query(LostAnimalsModel).filter(LostAnimalsModel.owner_id == user_id).all()
        existing_user = db.query(UsersModel).filter(UsersModel.id == user_id).first()
        if existing_user:
            if user['role'] == 'admin' or existing_user:
                response.delete_cookie('access_token')

                for animal in animal_model:
                    db.delete(animal)
                db.commit()

                db.delete(existing_user)
                db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
