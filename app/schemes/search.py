from pydantic import BaseModel
from enum import Enum


class AnimalGender(str, Enum):
    male = 'male'
    female = 'female'


class SearchModel(BaseModel):
    country: str
    city: str
    is_lost: bool
    shelters: list = []
    animals: list = []
    breed: str
    gender: AnimalGender
    is_rewarded: bool
    is_collar: bool

    class Config:
        json_schema_extra = {
            'example': {
                'country': '',
                'city': '',
                'is_lost': True,
                'shelters': [],
                'animals': [],
                'breed': '',
                'gender': 'male',
                'is_rewarded': True,
                'is_collar': True
            }
        }
