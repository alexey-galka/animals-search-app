from typing import Optional
from fastapi import APIRouter, status, HTTPException, Path, Query
from app.models.animals import LostAnimalsModel
from app.models.shelters import SheltersModel
from app.models.users import UsersModel
from app.schemes.users import CreateUserScheme
from app.shared.dependencies import user_dependency, db_dependency
from app.schemes.animals import LostAnimalsScheme

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/{user_id}', status_code=status.HTTP_200_OK)
async def read_profile(db: db_dependency, user_id: int = Path(gt=0)):
    if user_id:
        user = db.query(UsersModel).filter(UsersModel.id == user_id).first()
        if user:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
