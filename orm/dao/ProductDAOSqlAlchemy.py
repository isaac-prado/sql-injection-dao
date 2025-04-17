from sqlalchemy.orm import sessionmaker
from orm.db.database import getSession
from orm.model.model import Products

class ProductDAOSqlAlchemy:
    def __init__(self):
        self.session = getSession()
        
    def GetProductByName(self, product_name):
        try:
            product = self.session.query(Products).filter(Products.productname.ilike(product_name)).first()
            return product
        except Exception as e:
            print(f"Error getting product by name: {e}")
            return None