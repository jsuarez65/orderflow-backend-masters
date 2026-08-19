
from model.dtos import ProductDTO
from repositories.ProductRepository import ProductRepository
from configuration.LogConfiguration import LogConfiguration

productRepository = ProductRepository()

class ProductService:

    def __init__(self): 
        self.log = LogConfiguration.getLogger()
    
    def createProduct(self, product: ProductDTO):
        
        self.log.info("createProduct - Ingresa con product: ", body=product)

        if productRepository.findById(product.internalCode):
            self.log.warning("createProduct - El producto ya existe: ", body=product)
            return None

        return productRepository.save(product)

    def updateProduct(self, product: ProductDTO):
        
        self.log.info("updateProduct - Ingresa con product: ", body=product)

        if productRepository.existsById(product.internalCode):
            return productRepository.save(product)
        else:
            self.log.warning("updateProduct - El producto no existe: ", body=product)
            return False
