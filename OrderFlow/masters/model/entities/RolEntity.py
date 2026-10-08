from sqlalchemy import Column, String
from configuration.DatabaseConfiguration import Base


class RolEntity(Base):
    __tablename__ = 'rol'

    rol = Column(String(50), primary_key=True, nullable=False)

    def __repr__(self) -> str:
        return f"<RolEntity(rol='{self.rol}')>"