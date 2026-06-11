
import ProductRepository
import LogConfiguration

productRepository = ProductRepository()

class ProductService:

    def __init__(self): 
        self.log = LogConfiguration.getLogger()
    
    def createProduct(product):
        
        self.log.info("createProduct - Ingresa con product: ", body=product)
        return productRepository.insertProduct(product)

        