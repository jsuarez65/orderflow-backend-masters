from sqlalchemy import Column, String, ForeignKey
from configuration.DatabaseConfiguration import Base


class UserEntity(Base):
    __tablename__ = 'usuarios'

    username = Column(String(50), primary_key=True, nullable=False)
    password = Column(String(255), nullable=False)
    rol = Column(String(50), ForeignKey('rol.rol'), nullable=False)

    def __repr__(self) -> str:
        return f"<UserEntity(username='{self.username}', rol='{self.rol}')>"