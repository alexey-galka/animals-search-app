import datetime
from fastapi import APIRouter, HTTPException, status, Path
from app.models.animals import LostAnimalsModel
from app.models.users import UsersModel
from app.schemes.animals import ShelterLostAnimalsScheme
from app.shared.dependencies import user_dependency, db_dependency
from app.schemes.shelters import SheltersScheme
from app.models.shelters import SheltersModel

router = APIRouter(
    prefix='/shelters',
    tags=['Shelters']
)


@router.post('/', status_code=status.HTTP_204_NO_CONTENT)
async def create_new_shelter(user: user_dependency, db: db_dependency, shelter: SheltersScheme):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication is failed')

    if user.get('role') != 'shelter' and user['role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No permissions')

    shelter_model = SheltersModel(**shelter.model_dump())
    shelter_model.owner_id = user.get('id')
    db.add(shelter_model)
    db.commit()

    user_model = db.query(UsersModel).filter(UsersModel.id == user.get('id')).first()
    user_model.shelter_id = shelter_model.id
    db.add(user_model)
    db.commit()


@router.get('/{shelter_id}', status_code=status.HTTP_200_OK)
async def read_shelter(db: db_dependency, shelter_id: int = Path(gt=0)):
    if shelter_id:
        shelter_model = db.query(SheltersModel).filter(SheltersModel.id == shelter_id).first()
        if shelter_model:
            return shelter_model
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shelter not found')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shelter not found')


@router.put('/{shelter_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_shelter_info(user: user_dependency, db: db_dependency, shelter: SheltersScheme,
                              shelter_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication is failed')

    shelter_model = db.query(SheltersModel).filter(SheltersModel.id == shelter_id).first()

    if shelter_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shelter not found')

    if user['role'] == 'shelter' or user['role'] == 'admin':
        shelter_model.name = shelter.name
        shelter_model.description = shelter.description
        shelter_model.country = shelter.country
        shelter_model.city = shelter.city
        shelter_model.address = shelter.address
        shelter_model.phone_number = shelter.phone_number
        shelter_model.email = shelter.email
        shelter_model.updated_on = datetime.date.today()

        db.add(shelter_model)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No permissions')


@router.delete('/{shelter_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_shelter(
        user: user_dependency,
        db: db_dependency,
        shelter_id: int
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Authentication failed')

    shelter_model = db.query(SheltersModel).filter(SheltersModel.id == shelter_id).first()
    user_model = db.query(UsersModel).filter(UsersModel.shelter_id == shelter_id).all()
    animal_model = db.query(LostAnimalsModel).filter(LostAnimalsModel.shelter_id == shelter_id).all()
    if shelter_model:
        shelter_owner = db.query(SheltersModel).filter(SheltersModel.owner_id == user['id']).first()
        if shelter_owner or user['role'] == 'admin':
            for volunteer in user_model:
                volunteer.shelter_id = None
                db.add(volunteer)
            db.commit()

            for animal in animal_model:
                db.delete(animal)
            db.commit()

            db.delete(shelter_model)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No permissions')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shelter not found')


@router.post('/{shelter_id}/volunteers/{volunteer_id}', status_code=status.HTTP_201_CREATED)
async def add_new_volunteer_to_shelter(
        user: user_dependency,
        db: db_dependency,
        volunteer_id: int = Path(gt=0),
        shelter_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication is failed')

    shelter_model = db.query(SheltersModel).filter(SheltersModel.id == shelter_id).first()
    if shelter_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shelter not found')

    if (user.get('role') == 'shelter' and user.get('id') == shelter_model.owner_id) or user['role'] == 'admin':

        volunteer = db.query(UsersModel).filter(UsersModel.id == volunteer_id).first()
        if volunteer.shelter_id == shelter_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Volunteer is already existing')
        else:
            volunteer.shelter_id = shelter_id
            db.add(volunteer)
            db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No permissions')


@router.get('/{shelter_id}/volunteers', status_code=status.HTTP_200_OK)
async def read_all_shelter_volunteers(db: db_dependency, shelter_id: int = Path(gt=0)):
    if shelter_id:
        shelter = db.query(SheltersModel).filter(SheltersModel.id == shelter_id).first()
        if shelter:
            shelter_model = db.query(SheltersModel).filter(SheltersModel.id == shelter_id).first()
            if shelter_model is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shelter not found')

            existing_volunteers = db.query(UsersModel).where(SheltersModel.id == UsersModel.shelter_id).all()
            if len(existing_volunteers) < 1:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No volunteers added')
            return existing_volunteers
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shelter not found')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shelter not found')


@router.put('/{shelter_id}/volunteers/{volunteer_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_volunteer_from_shelter(
        user: user_dependency,
        db: db_dependency,
        shelter_id: int = Path(gt=0),
        volunteer_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication is failed')

    shelter_model = db.query(SheltersModel).filter(SheltersModel.id == shelter_id).first()
    if shelter_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shelter not found')

    if (user.get('role') == 'shelter' and user.get('id') == shelter_model.owner_id) or user['role'] == 'admin':

        volunteer = db.query(UsersModel).filter(UsersModel.id == volunteer_id).first()
        if volunteer.shelter_id == shelter_id:
            volunteer.shelter_id = None
            db.add(volunteer)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Volunteer not found')
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No permissions')


@router.post('/{shelter_id}/animals', status_code=status.HTTP_201_CREATED)
async def create_shelter_lost_animal(
        user: user_dependency,
        db: db_dependency,
        lost_animal: ShelterLostAnimalsScheme,
        shelter_id=int
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication is failed')

    shelter_model = db.query(SheltersModel).filter(SheltersModel.id == shelter_id).first()

    if shelter_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shelter not found')

    if user.get('role') == 'shelter' or user['role'] == 'admin':
        animal_model = LostAnimalsModel(**lost_animal.model_dump(), owner_id=shelter_model.id)
        animal_model.shelter_id = shelter_model.id
        animal_model.country_id = shelter_model.country
        animal_model.city_id = shelter_model.city

        db.add(animal_model)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No permissions')


@router.get('{shelter_id}/animals/all', status_code=status.HTTP_200_OK)
async def read_all_shelters_animals(
        db: db_dependency,
        shelter_id: int
):
    if shelter_id:
        shelter_model = db.query(SheltersModel).filter(SheltersModel.id == shelter_id).first()
        if shelter_model:
            return db.query(LostAnimalsModel).filter(LostAnimalsModel.shelter_id == shelter_id).all()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Animals not found')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shelter not found')


@router.get('{shelter_id}/animals/found', status_code=status.HTTP_200_OK)
async def read_shelter_found_animals(
        db: db_dependency,
        shelter_id: int
):
    if shelter_id:
        shelter_model = db.query(SheltersModel).filter(SheltersModel.id == shelter_id).first()
        if shelter_model:
            return db.query(LostAnimalsModel).filter(LostAnimalsModel.shelter_id == shelter_id, LostAnimalsModel.is_active == False).all()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Animals not found')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shelter not found')


@router.get('{shelter_id}/animals/lost', status_code=status.HTTP_200_OK)
async def read_shelter_lost_animals(
        db: db_dependency,
        shelter_id: int
):
    if shelter_id:
        shelter_model = db.query(SheltersModel).filter(SheltersModel.id == shelter_id).first()
        if shelter_model:
            return (db.query(LostAnimalsModel)
                    .filter(LostAnimalsModel.shelter_id == shelter_id, LostAnimalsModel.is_active == True).all())
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Animals not found')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shelter not found')


@router.put('/{shelter_id}/animals/{animal_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def update_lost_animal(
        user: user_dependency,
        db: db_dependency,
        lost_animal: ShelterLostAnimalsScheme,
        animal_id: int = Path(gt=0),
        shelter_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')

    shelter_model = db.query(SheltersModel).filter(SheltersModel.id == shelter_id).first()

    if user.get('role') == 'shelter' or user['role'] == 'admin':

        lost_animal_model = (db.query(LostAnimalsModel)
                             .filter(LostAnimalsModel.id == animal_id, LostAnimalsModel.shelter_id == shelter_model.id)
                             .first())

        if lost_animal_model:
            lost_animal_model.type = lost_animal.type
            lost_animal_model.breed = lost_animal.breed
            lost_animal_model.color = lost_animal.color
            lost_animal_model.gender = lost_animal.gender
            lost_animal_model.nickname = lost_animal.nickname
            lost_animal_model.photo_url = lost_animal.photo_url
            lost_animal_model.is_health = lost_animal.is_health
            lost_animal_model.special_instructions = lost_animal.special_instructions
            lost_animal_model.collar = lost_animal.collar
            lost_animal_model.collar_marks = lost_animal.collar_marks
            lost_animal_model.contact_name = lost_animal.contact_name
            lost_animal_model.contact_email = lost_animal.contact_email
            lost_animal_model.contact_phone = lost_animal.contact_phone
            lost_animal_model.is_active = lost_animal.is_active

            db.add(lost_animal_model)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Lost animal not found')
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No permissions')


@router.delete('/{shelter_id}/animals/{animal_id}/')
async def delete_lost_animal_from_shelter(
        user: user_dependency,
        db: db_dependency,
        animal_id: int = Path(gt=0),
        shelter_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')


    shelter_model = db.query(SheltersModel).filter(SheltersModel.id == shelter_id).first()

    if user.get('role') == 'shelter' or user['role'] == 'admin':

        lost_animal_model = (db.query(LostAnimalsModel)
                             .filter(LostAnimalsModel.id == animal_id, LostAnimalsModel.shelter_id == shelter_model.id)
                             .first())

        if lost_animal_model:
            db.delete(lost_animal_model)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Lost animal not found')
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No permissions')
