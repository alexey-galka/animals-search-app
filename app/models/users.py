from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class UsersModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    shelter_id = Column(Integer, ForeignKey('shelters.id'))
    username = Column(String, unique=True)
    avatar = Column(String)
    email = Column(String, unique=True)
    country = Column(String)
    city = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String)
    hashed_password = Column(String)

    shelters = relationship('SheltersModel', foreign_keys='UsersModel.shelter_id')

    def __init__(self, username, email, first_name, last_name, role, password, country, city, user_id=None):
        from app.shared.dependencies import bcrypt_context
        self.username = username
        self.email = email
        self.country = country
        self.city = city
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        if bcrypt_context:
            self.hashed_password = bcrypt_context.hash(password)
        self.id = user_id
