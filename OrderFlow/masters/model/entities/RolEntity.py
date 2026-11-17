from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from configuration.DatabaseConfiguration import Base


class RolEntity(Base):
    __tablename__ = 'rol'
    __table_args__ = {"extend_existing": True}

    rol = Column(String(50), primary_key=True, nullable=False)

    def __repr__(self) -> str:
        return f"<RolEntity(rol='{self.rol}')>"