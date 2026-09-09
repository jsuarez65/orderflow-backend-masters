from flask import Flask
from flask_cors import CORS
from configuration.LogConfiguration import LogConfiguration
from controllers.ProductController import ProductBlueprint
from controllers.ProviderController import ProviderBlueprint
from controllers.CustomerController import CustomerBlueprint
from flasgger import Swagger

masterMain = Flask(__name__)
swagger = Swagger(masterMain)

CORS(masterMain)

masterMain.register_blueprint(ProductBlueprint)
masterMain.register_blueprint(ProviderBlueprint)
masterMain.register_blueprint(CustomerBlueprint)

LogConfiguration.configure()

if __name__ == '__main__':
    masterMain.run(debug=True)



