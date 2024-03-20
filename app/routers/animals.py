from fastapi import APIRouter, status, HTTPException, Path
from app.models.animals import LostAnimalsModel
from app.models.users import UsersModel
from app.schemes.animals import LostAnimalsScheme
from app.shared.dependencies import user_dependency, db_dependency
from app.models.shelters import SheltersModel

router = APIRouter(
    prefix='/animals',
    tags=['Animals']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_new_lost_animal(
        user: user_dependency,
        db: db_dependency,
        lost_animal: LostAnimalsScheme):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication is failed')

    user_model = db.query(UsersModel).filter(UsersModel.id == user['id']).first()

    animal_model = LostAnimalsModel(**lost_animal.model_dump(), owner_id=user['id'])
    animal_model.country_id = user_model.country
    animal_model.city_id = user_model.city

    db.add(animal_model)
    db.commit()


@router.get('/{owner_id}/all', status_code=status.HTTP_200_OK)
async def read_all_user_lost_animals(db: db_dependency, owner_id: int = Path(gt=0)):
    user = db.query(UsersModel).filter(UsersModel.id == owner_id).first()
    if user:
        user_model = db.query(UsersModel).filter(UsersModel.id == owner_id).first()
        if user_model and user_model.role != 'shelter':
            return db.query(LostAnimalsModel).filter(LostAnimalsModel.owner_id == owner_id).all()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No animals found')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


@router.get('/{owner_id}/lost', status_code=status.HTTP_200_OK)
async def read_user_lost_animals(db: db_dependency, owner_id: int = Path(gt=0)):
    user = db.query(UsersModel).filter(UsersModel.id == owner_id).first()
    if user:
        user_model = db.query(UsersModel).filter(UsersModel.id == owner_id).first()
        if user_model and user_model.role != 'shelter':
            return db.query(LostAnimalsModel).filter(
                LostAnimalsModel.owner_id == owner_id,
                LostAnimalsModel.is_active == True
            ).all()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No animals found')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


@router.get('/{owner_id}/found', status_code=status.HTTP_200_OK)
async def read_user_found_animals(db: db_dependency, owner_id: int = Path(gt=0)):
    user = db.query(UsersModel).filter(UsersModel.id == owner_id).first()
    if user:
        user_model = db.query(UsersModel).filter(UsersModel.id == owner_id).first()
        if user_model and user_model.role != 'shelter':
            return db.query(LostAnimalsModel).filter(
                LostAnimalsModel.owner_id == owner_id,
                LostAnimalsModel.is_active == False
            ).all()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No animals found')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


@router.get('/{owner_id}/{animal_id}', status_code=status.HTTP_200_OK)
async def read_animal(
        db: db_dependency,
        owner_id: int = Path(gt=0),
        animal_id: int = Path(gt=0)
):
    user = db.query(UsersModel).filter(UsersModel.id == owner_id).first()
    if user:
        user_model = db.query(UsersModel).filter(UsersModel.id == owner_id).first()
        if user_model and user_model.role != 'shelter':
            lost_animal_model = (db.query(LostAnimalsModel)
                                 .filter(LostAnimalsModel.id == animal_id,
                                         LostAnimalsModel.owner_id == owner_id)
                                 .all())

            if lost_animal_model is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Lost animal not found')

            return lost_animal_model
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Animals not found')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


@router.put('/{owner_id}/{animal_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def update_lost_animal(
        user: user_dependency,
        db: db_dependency,
        lost_animal: LostAnimalsScheme,
        animal_id: int = Path(gt=0),
        owner_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')

    if owner_id:
        user = db.query(UsersModel).filter(UsersModel.id == owner_id).first()
        if user:
            owner = db.query(LostAnimalsModel).filter(LostAnimalsModel.owner_id == owner_id)

            if owner is None:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No permissions')

            lost_animal_model = (db.query(LostAnimalsModel)
                                 .filter(LostAnimalsModel.id == animal_id)
                                 .filter(LostAnimalsModel.owner_id == owner_id)
                                 .first())

            if lost_animal_model is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Lost animal not found')

            lost_animal_model.type = lost_animal.type
            lost_animal_model.breed = lost_animal.breed
            lost_animal_model.color = lost_animal.color
            lost_animal_model.gender = lost_animal.gender
            lost_animal_model.nickname = lost_animal.nickname
            lost_animal_model.photo_url = lost_animal.photo_url
            lost_animal_model.last_seen_place = lost_animal.last_seen_place
            lost_animal_model.last_seen_time = lost_animal.last_seen_time
            lost_animal_model.collar = lost_animal.collar
            lost_animal_model.collar_marks = lost_animal.collar_marks
            lost_animal_model.is_health = lost_animal.is_health
            lost_animal_model.is_rewards = lost_animal.is_rewards
            lost_animal_model.rewards_info = lost_animal.rewards_info
            lost_animal_model.contact_name = lost_animal.contact_name
            lost_animal_model.contact_email = lost_animal.contact_email
            lost_animal_model.contact_phone = lost_animal.contact_phone
            lost_animal_model.is_active = lost_animal.is_active

            db.add(lost_animal_model)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


@router.delete('/{owner_id}/{animal_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_lost_animal(
        user: user_dependency,
        db: db_dependency,
        animal_id: int = Path(gt=0),
        owner_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')

    if user['id'] != owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No permissions')

    if owner_id or user['role'] == 'admin':
        user = db.query(UsersModel).filter(UsersModel.id == owner_id).first()
        if user:
            owner = db.query(LostAnimalsModel).filter(LostAnimalsModel.owner_id == owner_id)

            if owner is None:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No permissions')

            lost_animal_model = (db.query(LostAnimalsModel)
                                 .filter(LostAnimalsModel.id == animal_id)
                                 .filter(LostAnimalsModel.owner_id == owner_id)
                                 .first())
            if lost_animal_model is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Lost animal not found')

            db.delete(lost_animal_model)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
