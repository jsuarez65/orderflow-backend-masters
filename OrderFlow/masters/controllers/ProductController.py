from flask import Blueprint, request
import ProductService
import LogConfiguration

ProductBlueprint = Blueprint('product', __name__, "url_prefix='/master/product'")

productService = ProductService()

@ProductBlueprint.route('', methods=['POST'])
def createProduct():

    log = LogConfiguration.getLogger()
    
    product = request.get_json()

    log.info("createProduct - Ingresa con product: ", body=product)

    if (productService.createProduct(product) == True):
        return {"message": "El producto se ingresó correctamente"}, 200
    else:
        return {"message": "Error al ingresar el producto"}, 500
