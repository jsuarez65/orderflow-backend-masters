from sqlalchemy.exc import IntegrityError

from configuration.DatabaseConfiguration import SessionLocal
from configuration.LogConfiguration import LogConfiguration
from model.entities.UserEntity import UserEntity
from model.dto import userDTO
from mappers.UsersMappers import UserMapper


class UsersRepository:

    def __init__(self, log=None):
        self.log = log or LogConfiguration.getLogger()

    def save(self, user: userDTO) -> userDTO | None:
        session = SessionLocal()
        try:
            entity = UserMapper.toEntity(user)
            session.merge(entity)
            session.commit()
            return UserMapper.toDTO(entity)
        except Exception as ex:
            session.rollback()
            self.log.error(f"save - Error guardando usuario: {str(ex)}")
            return None
        finally:
            session.close()

    def findByUsername(self, username: str) -> userDTO | None:
        session = SessionLocal()
        try:
            entity = session.query(UserEntity).filter(
                UserEntity.username == username
            ).first()
            return UserMapper.toDTO(entity)
        except Exception as ex:
            self.log.error(f"findByUsername - Error: {str(ex)}")
            return None
        finally:
            session.close()

    def getAll(self) -> list[userDTO]:
        session = SessionLocal()
        try:
            entities = session.query(UserEntity).all()
            return UserMapper.toListDTO(entities)
        except Exception as ex:
            self.log.error(f"getAll - Error: {str(ex)}")
            return []
        finally:
            session.close()

    def update(self, usernameActual: str, user: userDTO) -> bool:
        session = SessionLocal()
        try:
            entity = session.query(UserEntity).filter(
                UserEntity.username == usernameActual
            ).first()
            if not entity:
                return False

            if user.username and user.username != usernameActual:
                duplicate = session.query(UserEntity).filter(
                    UserEntity.username == user.username
                ).first()
                if duplicate:
                    return False
                entity.username = user.username

            if user.password:
                entity.password = user.password
            if user.rol:
                entity.rol = user.rol

            session.commit()
            return True
        except Exception as ex:
            session.rollback()
            self.log.error(f"update - Error: {str(ex)}")
            return False
        finally:
            session.close()

    def delete(self, username: str) -> bool:
        session = SessionLocal()
        try:
            entity = session.query(UserEntity).filter(
                UserEntity.username == username
            ).first()
            if not entity:
                return False
            session.delete(entity)
            session.commit()
            return True
        except Exception as ex:
            session.rollback()
            self.log.error(f"delete - Error: {str(ex)}")
            return False
        finally:
            session.close()