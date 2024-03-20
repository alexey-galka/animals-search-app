from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class SheltersModel(Base):
    __tablename__ = 'shelters'

    id = Column(Integer, index=True, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    avatar = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    description = Column(String)
    country = Column(String)
    city = Column(String)
    shelter_lat = Column(String)
    shelter_lon = Column(String)
    address = Column(String)
    phone_number = Column(String)
    email = Column(String)
    volunteer_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    animal_id = Column(Integer, ForeignKey('animals.id', ondelete='CASCADE'))
    added_on = Column(DateTime(timezone=True), default=func.now())
    updated_on = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    users = relationship('UsersModel', foreign_keys='SheltersModel.owner_id')
    volunteers = relationship('UsersModel', foreign_keys='SheltersModel.volunteer_id')
    animals = relationship('LostAnimalsModel', foreign_keys='SheltersModel.animal_id')
