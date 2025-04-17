from sqlalchemy.orm import sessionmaker
from orm.db.database import getConnection
from orm.model.model import Products

class ProductDAOSqlAlchemy:
    def __init__(self):
        self.connection = getConnection()
        self.Session = sessionmaker(bind=self.connection)
        
    def GetProductByName(self, product_name):
        session = self.Session()
        try:
            product = session.query(Products).filter(Products.productname.ilike(product_name)).first()
            return product
        except Exception as e:
            print(f"Error getting product by name: {e}")
            return None
        finally:
            session.close()