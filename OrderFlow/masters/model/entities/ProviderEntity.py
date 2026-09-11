from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from configuration.DatabaseConfiguration import Base

class ProviderEntity(Base):
    __tablename__ = 'provider'

    