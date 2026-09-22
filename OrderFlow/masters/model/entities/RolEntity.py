from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean
#from sqlalchemy.ext.declarative import declarative_base # ORM
from configuration.DatabaseConfiguration import Base

#Base = declarative_base()

class RolEntity(Base):
    __tablename__ = 'rol'

    rol = Column(String(100), primary_key=True)