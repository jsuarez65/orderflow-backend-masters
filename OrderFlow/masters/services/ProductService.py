
from repositories.ProductRepository import ProductRepository
from configuration.LogConfiguration import LogConfiguration

productRepository = ProductRepository()

class ProductService:

    def __init__(self): 
        self.log = LogConfiguration.getLogger()
    
    def createProduct(self, product):
        
        self.log.info("createProduct - Ingresa con product: ", body=product)

        if productRepository.findById(product['codigo_interno']):
            self.log.warning("createProduct - El producto ya existe: ", body=product)
            return False

        return productRepository.save(product)

    def updateProduct(self, product):
        
        self.log.info("updateProduct - Ingresa con product: ", body=product)

        if productRepository.findById(product['codigo_interno']):
            return productRepository.save(product)
        else:
            self.log.warning("updateProduct - El producto no existe: ", body=product)
            return False
