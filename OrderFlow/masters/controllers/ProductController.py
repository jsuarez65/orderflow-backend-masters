from dataclasses import asdict
from logging import log

from flask import Blueprint, request
from model.dtos.ProductDTO import ProductDTO
from services.ProductService import ProductService
from configuration.LogConfiguration import LogConfiguration
from configuration.DatabaseConfiguration import sessionLocal

ProductBlueprint = Blueprint('product', __name__, url_prefix='/master/product')

@ProductBlueprint.route('', methods=['GET'])
def getAll() -> tuple[list[dict], int]:
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
    
    log.info("getAll - Ingresa a recuperar todos los productos")

    session = sessionLocal()
    productService = ProductService(log, session=session)
    products = productService.findAll()

    return {products}, 200

@ProductBlueprint.route('', methods=['POST'])
def create() -> tuple[dict, int]:
    
    session = sessionLocal()
    log = LogConfiguration.getLogger()
    
    product = ProductDTO(**request.get_json())

    productService = ProductService(log, session=session)

    log.info("create - Ingresa con producto: ", body=product)

    productCreated = productService.create(product)

    if (productCreated is not None):
        return asdict(productCreated), 200
    else:
        return {"message": "No se puede crear el producto debido a que el mismo ya existe"}, 500

@ProductBlueprint.route('', methods=['PUT'])
def update() -> tuple[dict, int]:

    session = sessionLocal()
    log = LogConfiguration.getLogger()

    productService = ProductService(log, session=session)

    product = ProductDTO(**request.get_json())
    
    log.info("update - Ingresa con producto: ", body=product)

    productUpdated = productService.update(product)
    if (productUpdated is not None):
        return asdict(productUpdated), 200
    else:
        return {"message": "El producto a actualizar no existe"}, 500
