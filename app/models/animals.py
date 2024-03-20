from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class LostAnimalsModel(Base):
    __tablename__ = 'animals'

    id = Column(Integer, index=True, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    shelter_id = Column(Integer, ForeignKey('shelters.id', ondelete='CASCADE'))
    type = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    color = Column(String)
    gender = Column(String)
    nickname = Column(String, nullable=False)
    photo_url = Column(String)
    country_id = Column(String, ForeignKey('users.country', ondelete='CASCADE'))
    city_id = Column(String, ForeignKey('users.city', ondelete='CASCADE'))
    last_seen_place = Column(String)
    place_lat = Column(String)
    place_lon = Column(String)
    is_health = Column(Boolean)
    special_instructions = Column(String)
    last_seen_time = Column(String)
    collar = Column(Boolean)
    collar_marks = Column(String)
    is_rewards = Column(Boolean)
    rewards_info = Column(String)
    contact_name = Column(String)
    contact_email = Column(String)
    contact_phone = Column(String)
    is_active = Column(Boolean, default=True)

    owner = relationship('UsersModel', foreign_keys='LostAnimalsModel.owner_id')
    shelters = relationship('SheltersModel', foreign_keys='LostAnimalsModel.shelter_id')
    country = relationship('UsersModel', foreign_keys='LostAnimalsModel.country_id')
    city = relationship('UsersModel', foreign_keys='LostAnimalsModel.city_id')
