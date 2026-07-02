from flask import Flask
from flask_cors import CORS
from configuration.LogConfiguration import LogConfiguration
from controllers.ProductController import ProductBlueprint
from controllers.ProviderController import ProviderBlueprint
from controllers.PermisosController import PermissionBlueprint
from controllers.RolController import rolBlueprint
from controllers.UsersController import usersBlueprint

masterMain = Flask(__name__)
CORS(masterMain)

masterMain.register_blueprint(ProductBlueprint)
masterMain.register_blueprint(ProviderBlueprint)
masterMain.register_blueprint(PermissionBlueprint)
masterMain.register_blueprint(rolBlueprint)
masterMain.register_blueprint(usersBlueprint)



LogConfiguration.configure()

if __name__ == '__main__':
    masterMain.run(debug=True, port=5000)


