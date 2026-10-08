
    
from flask import Flask
from flasgger import Swagger
from flask_cors import CORS

from configuration.LogConfiguration import LogConfiguration
LogConfiguration.configure()
log = LogConfiguration.getLogger()

from controllers.PermissionController import permissionBp
from controllers.RolController import rolBp
from controllers.UsersController import userBp


masterMain = Flask(__name__)

swagger = Swagger(masterMain)
CORS(masterMain)

masterMain.register_blueprint(permissionBp)
masterMain.register_blueprint(rolBp)
masterMain.register_blueprint(userBp)


if __name__ == '__main__':
    log.info("Iniciando el servidor de desarrollo en http://localhost:5000...")
    masterMain.run(debug=True, host='0.0.0.0', port=5000)


