from flask import Flask
from flask_cors import CORS
import LogConfiguration
from routes.ProductController import ProductBlueprint
from routes.ProviderController import ProviderBlueprint

masterMain = Flask(__name__)
CORS(masterMain)

masterMain.register_blueprint(ProductBlueprint)
masterMain.register_blueprint(ProviderBlueprint)

LogConfiguration.configure()

if __name__ == '__main__':
    masterMain.run(debug=True)


