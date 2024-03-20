from typing import Optional

from fastapi import APIRouter, status, HTTPException, Query
from app.shared.dependencies import user_dependency, db_dependency
from app.models.users import UsersModel
from app.models.animals import LostAnimalsModel
from app.models.shelters import SheltersModel

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


@router.get('/users', status_code=status.HTTP_200_OK, description='Get all users')
async def get_all_users(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No permissions')
    return db.query(UsersModel).all()


@router.get('/animals', status_code=status.HTTP_200_OK, description='Get all lost animals')
async def get_all_animals(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No permissions')

    return db.query(LostAnimalsModel).all()


@router.get('/shelters', status_code=status.HTTP_200_OK)
async def get_all_shelters(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No permissions')

    return db.query(SheltersModel).all()


@router.get('/volunteers', status_code=status.HTTP_200_OK)
async def get_all_volunteers(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No permissions')

    return db.query(UsersModel).where(UsersModel.role == 'volunteer').all()


@router.get('/owners', status_code=status.HTTP_200_OK)
async def get_all_animal_owners(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No permissions')

    return db.query(UsersModel).filter(UsersModel.role == 'searcher').all()
