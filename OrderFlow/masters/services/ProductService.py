
from exceptions.product_exceptions import ProductAlreadyExistsException, ProductCreationException, ProductNotFoundException, ProductUpdateException
from mappers.ProductMapper import ProductMapper
from model.dtos import ProductDTO
from repositories.ProductRepository import ProductRepository


class ProductService:

    def __init__(self, log, session): 
        self.log = log
        self.session = session
        self.productRepository = ProductRepository(log, session)

    def findAll(self) -> list[ProductDTO]:

        self.log.info("findAll - Ingresa a recuperar todos los productos")

        productEntities = self.productRepository.findAll()
        return ProductMapper.toListDTO(productEntities)
    
    def create(self, product: ProductDTO) -> ProductDTO | None:
        
        self.log.info("create - Ingresa con producto: ", body=product)

        
        if self.productRepository.existsById(product.internalCode):
            raise ProductAlreadyExistsException(
                f"El producto con código interno '{product.internalCode}' ya existe.")

        try:
        
            productToCreate = ProductMapper.toEntity(product)
            productCreated = ProductMapper.toDTO(self.productRepository.save(productToCreate))

            self.session.commit()
            return productCreated
        
        except Exception as ex:
            self.session.rollback()
            self.log.error(f"create - Error al crear el producto: {str(ex)}")
            raise ProductCreationException(
                f"Error al crear el producto: {str(ex)}") from ex

    def update(self, product: ProductDTO) -> ProductDTO | None:
        
        self.log.info("update - Ingresa con producto: ", body=product)

        if not self.productRepository.existsById(product.internalCode):
            raise ProductNotFoundException(
                f"El producto con código interno '{product.internalCode}' no existe.")

        try:

            productToUpdate = ProductMapper.toEntity(product)
            productUpdated = ProductMapper.toDTO(self.productRepository.save(productToUpdate))

            self.session.commit()
            return productUpdated
        

        except Exception as ex:
            self.session.rollback()
            self.log.error(f"update - Error al actualizar el producto: {str(ex)}")
            raise ProductUpdateException(
                f"Error al actualizar el producto: {str(ex)}") from ex   
        
