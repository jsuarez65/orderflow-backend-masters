from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from configuration.LogConfiguration import LogConfiguration
from controllers.ProductController import ProductBlueprint
from controllers.ProviderController import ProviderBlueprint
from controllers.PermissionController import PermissionBlueprint
from controllers.RolController import roleBlueprint
from controllers.UsersController import usersBlueprint
from controllers.RolController import roleBlueprint
from controllers.UsersController import usersBlueprint

masterMain = Flask(__name__)

swagger = Swagger(masterMain)

CORS(masterMain)

masterMain.register_blueprint(ProductBlueprint)
masterMain.register_blueprint(ProviderBlueprint)
masterMain.register_blueprint(PermissionBlueprint)
masterMain.register_blueprint(roleBlueprint)
masterMain.register_blueprint(usersBlueprint)



LogConfiguration.configure()

if __name__ == '__main__':
    masterMain.run(debug=True, port=5000)


