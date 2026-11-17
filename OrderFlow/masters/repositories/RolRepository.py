from model.entities.RolEntity import RolEntity



class RolRepository:

    def __init__(self, log, session):
        self.session = session
        self.log = log

    def findAll(self) -> list[RolEntity]:
        return self.session.query(RolEntity).all()
    
    def save(self, rol: RolEntity) -> RolEntity:
        rolFound = self._findByRol(rol.rol)

        if rolFound:
            self.log.warning(
                f"save - El rol ya existe, se procederá a actualizarlo: {rol}"
            )
            return self._update(rolFound, rol)

        return self._insert(rol)
    
    def existsByRol(self, rol: str) -> bool:
        return self._findByRol(rol) is not None
    
    def _findByRol(self, rol: str) -> RolEntity | None:
        return (
            self.session.query(RolEntity)
            .filter(RolEntity.rol == rol)
            .first()
        )
        
    def _insert(self, rol: RolEntity) -> RolEntity:
        self.session.add(rol)
        return rol
    
    def _update(self, entityToUpdate: RolEntity, entity: RolEntity) -> RolEntity:
        entityToUpdate.rol = entity.rol

        return entityToUpdate