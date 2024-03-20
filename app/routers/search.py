from fastapi import APIRouter, status, HTTPException, Query, Depends

from app.schemes.search import SearchModel
from app.shared.dependencies import db_dependency
from typing import Optional
from app.models.animals import LostAnimalsModel
from app.models.users import UsersModel
from app.models.shelters import SheltersModel

router = APIRouter(
    prefix='/search',
    tags=['Search'],
)


@router.post('/', status_code=status.HTTP_200_OK)
async def read_lost_animals(db: db_dependency, search_request: SearchModel):
    query = db.query(LostAnimalsModel)

    if search_request.country:
        query = query.filter(LostAnimalsModel.country.has(country=search_request.country))
    if search_request.city:
        query = query.filter(LostAnimalsModel.city.has(city=search_request.city))
    if search_request.is_lost is not None:
        query = query.filter(LostAnimalsModel.is_active == search_request.is_lost)
    if search_request.shelters:
        query = query.filter(LostAnimalsModel.shelter_id.in_(search_request.shelters)).all()
    if search_request.animals:
        query = query.filter(LostAnimalsModel.type.in_(search_request.animals)).all()
    if search_request.breed:
        query = query.filter(LostAnimalsModel.breed == search_request.breed)
    if search_request.gender:
        query = query.filter(LostAnimalsModel.gender == search_request.gender)
    if search_request.is_rewarded is not None:
        query = query.filter(LostAnimalsModel.is_rewards == search_request.is_rewarded)
    if search_request.is_collar is not None:
        query = query.filter(LostAnimalsModel.collar == search_request.is_collar)

    result = query.all()
    return result
