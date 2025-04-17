from noorm.dao.ProductDAO import ProductDAO

class ProductController:
    def __init__(self, product_dao):
        self.ProductDAO = ProductDAO()
        
    def GetProductByName(self, name):
        product = self.ProductDAO.GetProductByName(name)
        
        if not product:
            return ValueError("Product not found")
        
        print(product)        
        return product