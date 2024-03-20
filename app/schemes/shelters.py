from pydantic import BaseModel, EmailStr


class SheltersScheme(BaseModel):
    name: str
    description: str
    country: str
    city: str
    address: str
    phone_number: str
    email: EmailStr

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                'name': 'Happy Paws Shelter',
                'description': 'A loving home for abandoned animals',
                'country': 'UK',
                'city': 'London',
                'address': '123 Pet Lane, Cityville',
                'phone_number': '+1 555-1234',
                'email': 'info@happypawsshelter.com',
            }
        }
