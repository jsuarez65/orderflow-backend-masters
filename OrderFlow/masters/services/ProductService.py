
from model.dtos import ProductDTO
from repositories.ProductRepository import ProductRepository


class ProductService:

    def __init__(self, log, session): 
        self.log = log
        self.productRepository = ProductRepository(session)
    
    def createProduct(self, product: ProductDTO):
        
        self.log.info("createProduct - Ingresa con product: ", body=product)

        if self.productRepository.findById(product.internalCode):
            self.log.warning("createProduct - El producto ya existe: ", body=product)
            return None

        return self.productRepository.save(product)

    def updateProduct(self, product: ProductDTO):
        
        self.log.info("updateProduct - Ingresa con product: ", body=product)

        if self.productRepository.existsById(product.internalCode):
            return self.productRepository.save(product)
        else:
            self.log.warning("updateProduct - El producto no existe: ", body=product)
            return False
