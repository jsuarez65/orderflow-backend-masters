from sqlalchemy.orm import Session

from model.entities.UserEntity import UserEntity


class UserRepository:

    def __init__(self, log, session: Session):
        self.session = session
        self.log = log

    def findAll(self) -> list[UserEntity]:
        return self.session.query(UserEntity).all()

    def findByUsername(self, username: str) -> UserEntity | None:
        return self._findByUsername(username)

    def save(self, user: UserEntity) -> UserEntity:
        self.session.add(user)
        return user

    def existsByUsername(self, username: str) -> bool:
        return self._findByUsername(username) is not None

    def update(self, username: str, user: UserEntity) -> UserEntity | None:
        userToUpdate = self._findByUsername(username)
        if userToUpdate is None:
            return None

        userToUpdate.username = user.username
        userToUpdate.password = user.password
        userToUpdate.rol = user.rol
        return userToUpdate

    def delete(self, username: str) -> UserEntity | None:
        user = self._findByUsername(username)
        if user is None:
            return None

        self.session.delete(user)
        return user

    def _findByUsername(self, username: str) -> UserEntity | None:
        return (
            self.session.query(UserEntity)
            .filter(UserEntity.username == username)
            .first()
        )
