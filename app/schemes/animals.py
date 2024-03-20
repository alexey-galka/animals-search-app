from pydantic import BaseModel, EmailStr, Field


class LostAnimalsScheme(BaseModel):
    type: str
    breed: str
    color: str
    gender: str
    nickname: str = Field(min_length=2, max_length=15)
    photo_url: str
    is_health: bool
    last_seen_place: str
    last_seen_time: str
    collar: bool
    collar_marks: str
    is_rewards: bool
    is_active: bool
    rewards_info: str
    contact_name: str
    contact_email: EmailStr
    contact_phone: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                "type": "dog",
                "breed": "Labrador Retriever",
                "color": "Golden",
                "gender": "male",
                "nickname": "Maxi",
                'is_health': True,
                "photo_url": "https://example.com/max_photo.jpg",
                "last_seen_place": "City Park",
                "last_seen_time": "2024-03-11T14:30:00",
                "collar": True,
                "collar_marks": "Blue collar with a tag",
                "is_rewards": True,
                "rewards_info": "Generous reward for safe return",
                'is_active': True,
                "contact_name": "John Smith",
                "contact_email": "john.smith@example.com",
                "contact_phone": "+1234567890",
            }
        }


class ShelterLostAnimalsScheme(BaseModel):
    type: str
    breed: str
    color: str
    gender: str
    nickname: str = Field(min_length=2, max_length=15)
    photo_url: str
    is_health: bool
    special_instructions: str
    collar: bool
    collar_marks: str
    contact_name: str
    contact_email: EmailStr
    contact_phone: str
    is_active: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                "type": "dog",
                "breed": "Labrador Retriever",
                "color": "Golden",
                "gender": "male",
                "nickname": "Maxi",
                'is_health': True,
                "photo_url": "https://example.com/max_photo.jpg",
                'special_instructions': 'Do not eat cats',
                "collar": True,
                "collar_marks": "Blue collar with a tag",
                "contact_name": "John Smith",
                "contact_email": "john.smith@example.com",
                "contact_phone": "+1234567890",
                'is_active': True
            }
        }
