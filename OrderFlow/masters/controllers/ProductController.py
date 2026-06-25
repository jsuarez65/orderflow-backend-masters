from flask import Blueprint, request
from services.ProductService import ProductService
from configuration.LogConfiguration import LogConfiguration

ProductBlueprint = Blueprint('product', __name__, url_prefix='/master/product')

productService = ProductService()

@ProductBlueprint.route('', methods=['POST'])
def createProduct():

    log = LogConfiguration.getLogger()
    
    product = request.get_json()

    log.info("createProduct - Ingresa con product: ", body=product)

    productCreated = productService.createProduct(product)
    if (productCreated is not None):
        return productCreated, 200
    else:
        return {"message": "Error al ingresar el producto"}, 500

@ProductBlueprint.route('', methods=['PUT'])
def updateProduct():

    log = LogConfiguration.getLogger()
    
    product = request.get_json()

    log.info("updateProduct - Ingresa con product: ", body=product)

    productUpdated = productService.updateProduct(product)
    if (productUpdated is not None):
        return productUpdated, 200
    else:
        return {"message": "Error al actualizar el producto"}, 500
