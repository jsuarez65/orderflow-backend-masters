from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean
#from sqlalchemy.ext.declarative import declarative_base # ORM
from configuration.DatabaseConfiguration import Base

#Base = declarative_base()

class UserEntity(Base):
    __tablename__ = 'usuarios'

    username = Column(String(100), primary_key=True)
    password = Column(String(100))
    rol = Column(String(100))