from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class UserRole(str, Enum):
    admin = 'admin'
    volunteer = 'volunteer'
    owner = 'owner'
    shelter = 'shelter'


class CreateUserScheme(BaseModel):
    username: str = Field(min_length=4, max_length=10)
    email: EmailStr
    country: str
    city: str
    first_name: str
    last_name: str
    role: UserRole
    password: str = Field(min_length=4, max_length=20)

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                'username': 'admin',
                'email': 'awesome_user@domain.com',
                'country': 'UK',
                'city': 'London',
                'first_name': 'John',
                'last_name': 'Doe',
                'role': 'admin',
                'password': 'password'
            }
        }
