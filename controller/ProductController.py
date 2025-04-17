class ProductController:
    def __init__(self, product_dao):
        self.ProductDAO = product_dao
        
    def GetProductByName(self, name):
        product = self.ProductDAO.GetProductByName(name)
        
        if not product:
            return ValueError("Product not found")
        return product