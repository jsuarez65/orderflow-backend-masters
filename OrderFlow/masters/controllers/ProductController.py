from flask import Blueprint, request
from model.dtos.ProductDTO import ProductDTO
from services.ProductService import ProductService
from configuration.LogConfiguration import LogConfiguration


ProductBlueprint = Blueprint('product', __name__, url_prefix='/master/product')

productService = ProductService()

@ProductBlueprint.route('', methods=['GET'])
def getProducts() -> list[ProductDTO]:
    """ 
    Permite recuperar todos los productos registrados en la base de datos.
    ---
    responses:
      200:
        description: Lista de ProductDTO.
        schema:
          type: array
          items:
            $ref: '#/definitions/ProductDTO'
    definitions:
      ProductDTO:
        type: object
        properties:
          internalCode:
            type: string
            example: "PROD-001"
          sku:
            type: string
            example: "SKU-12345"
          barcode:
            type: string
            example: "7791234567890"
          description:
            type: string
            example: "Descripción del producto"
          unitMeasurements:
            type: string
            example: "Unidades"
          weight:
            type: number
            format: float
            example: 1.5
          dimensions:
            type: string
            example: "10x20x30 cm"
          minimumStock:
            type: number
            format: float
            example: 10.0
          maximumStock:
            type: number
            format: float
            example: 100.0
          reorderPoint:
            type: number
            format: float
            example: 20.0
          productCategoriesId:
            type: integer
            example: 5
          providerTaxId:
            type: string
            example: "30-12345678-9"
    """
            
    log = LogConfiguration.getLogger()
    
    log.info("getProducts - Ingresa a obtener productos")
    return {"message": "ok"}, 200

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
    
    product = ProductDTO(**request.get_json())

    product.internalCode

    log.info("updateProduct - Ingresa con product: ", body=product)

    productUpdated = productService.updateProduct(product)
    if (productUpdated is not None):
        return productUpdated, 200
    else:
        return {"message": "Error al actualizar el producto"}, 500
