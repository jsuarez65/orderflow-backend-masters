        
from repositories.UsersRepository import UsersRepository
from configuration.LogConfiguration import LogConfiguration
from werkzeug.security import generate_password_hash

usersRepository = UsersRepository()

class UsersService:

    def __init__(self): 
        self.log = LogConfiguration.getLogger()
    
    def createUser(self, user):
        self.log.info("createUser - Ingresa con usuario: ", body=user)
        user['password'] = generate_password_hash(user['password'])
        return usersRepository.insertUser(user)
    
    def getUser(self, username):
        self.log.info("getUser - Ingresa con nombre: ", body=username)
        return usersRepository.findByUsername(username)
    
    def updateUser(self, usernameActual, userData):
        self.log.info(f"updateUser - Actualizar usuario '{usernameActual}'")
        userData['password'] = generate_password_hash(userData['password'])
        return usersRepository.updateUser(usernameActual, userData)
    
    def deleteUser(self, username):
        self.log.info("deleteUser - Eliminar usuario: ", body=username)
        return usersRepository.deleteUser(username)