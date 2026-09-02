from flask import Blueprint, request
from services.ProductService import ProductService
from configuration.LogConfiguration import LogConfiguration

ProductBlueprint = Blueprint('product', __name__, url_prefix='/master/product')

productService = ProductService()

@ProductBlueprint.route('/', methods=['POST'])
def createProduct():

    log = LogConfiguration.getLogger()
    
    product = request.get_json()

    log.info("createProduct - Ingresa con product: ", body=product)

    if (productService.createProduct(product) == True):
        return {"message": "El producto se ingresó correctamente"}, 200
    else:
        return {"message": "Error al ingresar el producto"}, 500
    
    
@ProductBlueprint.route('', methods=['PUT'])
def updateProduct():

    log = LogConfiguration.getLogger()
    
    product = request.get_json()

    log.info("updateProduct - Ingresa con product: ", body=product)

    if (productService.updateProduct(product) == True):
        return {"message": "El producto se actualizó correctamente"}, 200
    else:
        return {"message": "Error al actualizar el producto"}, 500

@ProductBlueprint.route('/<int:product_id>', methods=['GET'])
def getProduct(product_id):

    log = LogConfiguration.getLogger()

    log.info(f"getProduct - Ingresa a obtener el producto: {product_id}")

    productFound = productService.getProduct(product_id)

    if productFound:
        return productFound, 200
    else:
        return {"message": "Producto no encontrado"}, 404