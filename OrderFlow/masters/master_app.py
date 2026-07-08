from flask import Flask
from flask_cors import CORS
from configuration.LogConfiguration import LogConfiguration
from controllers.ProductController import ProductBlueprint
from controllers.ProviderController import ProviderBlueprint

masterMain = Flask(__name__)
CORS(masterMain)

masterMain.register_blueprint(ProductBlueprint)
masterMain.register_blueprint(ProviderBlueprint)

LogConfiguration.configure()

if __name__ == '__main__':
    masterMain.run(debug=True)


