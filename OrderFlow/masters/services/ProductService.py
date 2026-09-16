
from OrderFlow.masters.mappers.ProductMapper import ProductMapper
from model.dtos import ProductDTO
from repositories.ProductRepository import ProductRepository


class ProductService:

    def __init__(self, log, session): 
        self.log = log
        self.productRepository = ProductRepository(session)

    def findAll(self) -> list[ProductDTO]:

        productEntities = self.productRepository.findAll()
        return ProductMapper.toListDTO(productEntities)
    
    def create(self, product: ProductDTO) -> ProductDTO | None:
        
        self.log.info("create - Ingresa con product: ", body=product)

        if self.productRepository.existsById(product.internalCode):
            self.log.warning("create - El producto ya existe: ", body=product)
            return None

        productToCreate = ProductMapper.toEntity(product)
        return ProductMapper.toDTO(self.productRepository.save(productToCreate))

    def update(self, product: ProductDTO) -> ProductDTO | None:
        
        self.log.info("update - Ingresa con product: ", body=product)

        if not self.productRepository.existsById(product.internalCode):
            self.log.warning("update - El producto no existe: ", body=product)
            return None

        productToUpdate = ProductMapper.toEntity(product)
        return ProductMapper.toDTO(self.productRepository.save(productToUpdate))
