
from repositories.ProductRepository import ProductRepository
from configuration.LogConfiguration import LogConfiguration

productRepository = ProductRepository()

class ProductService:

    def __init__(self): 
        self.log = LogConfiguration.getLogger()
    
    def createProduct(self, product):
        
        self.log.info("createProduct - Ingresa con product: ", body=product)
        return productRepository.insertProduct(product)

        