from enum import Enum

from sqlalchemy.exc import IntegrityError

from configuration.DatabaseConfiguration import SessionLocal
from configuration.LogConfiguration import LogConfiguration
from model.entities.RolEntity import RolEntity
from model.dto import rolDTO
from mappers.RolMappers import RolMapper


class DeleteResult(Enum):
    OK = "OK"
    NOT_FOUND = "NOT_FOUND"
    IN_USE = "IN_USE"
    ERROR = "ERROR"


class RolRepository:

    def __init__(self, log=None):
        self.log = log or LogConfiguration.getLogger()

    def save(self, rol: rolDTO) -> rolDTO | None:
        session = SessionLocal()
        try:
            entity = RolMapper.toEntity(rol)

            existing = session.query(RolEntity).filter(
                RolEntity.rol == entity.rol
            ).first()
            if existing:
                self.log.warning("save - El rol ya existe: ", body=rol.rol)
                return None

            session.add(entity)
            session.commit()
            return RolMapper.toDTO(entity)
        except Exception as ex:
            session.rollback()
            self.log.error(f"save - Error guardando rol: {str(ex)}")
            return None
        finally:
            session.close()

    def findByName(self, rol: str) -> rolDTO | None:
        session = SessionLocal()
        try:
            entity = session.query(RolEntity).filter(RolEntity.rol == rol).first()
            return RolMapper.toDTO(entity)
        except Exception as ex:
            self.log.error(f"findByName - Error: {str(ex)}")
            return None
        finally:
            session.close()

    def getAll(self) -> list[rolDTO]:
        session = SessionLocal()
        try:
            entities = session.query(RolEntity).all()
            return RolMapper.toListDTO(entities)
        except Exception as ex:
            self.log.error(f"getAll - Error: {str(ex)}")
            return []
        finally:
            session.close()

    def update(self, rolActual: str, rolNuevo: rolDTO) -> bool:
        session = SessionLocal()
        try:
            entity = session.query(RolEntity).filter(
                RolEntity.rol == rolActual
            ).first()
            if not entity:
                return False

            if rolNuevo.rol and rolNuevo.rol != rolActual:
                duplicate = session.query(RolEntity).filter(
                    RolEntity.rol == rolNuevo.rol
                ).first()
                if duplicate:
                    return False
                entity.rol = rolNuevo.rol

            session.commit()
            return True
        except Exception as ex:
            session.rollback()
            self.log.error(f"update - Error: {str(ex)}")
            return False
        finally:
            session.close()

    def delete(self, rol: str) -> DeleteResult:
        session = SessionLocal()
        try:
            entity = session.query(RolEntity).filter(RolEntity.rol == rol).first()
            if not entity:
                return DeleteResult.NOT_FOUND

            session.delete(entity)
            session.commit()
            return DeleteResult.OK

        except IntegrityError as ex:
            session.rollback()
            # 23503 = foreign_key_violation
            if getattr(getattr(ex, 'orig', None), 'pgcode', None) == '23503':
                self.log.warning(
                    f"delete - El rol '{rol}' está asignado a usuarios, no se puede eliminar"
                )
                return DeleteResult.IN_USE
            self.log.error(f"delete - IntegrityError: {str(ex)}")
            return DeleteResult.ERROR

        except Exception as ex:
            session.rollback()
            self.log.error(f"delete - Error: {str(ex)}")
            return DeleteResult.ERROR
        finally:
            session.close()