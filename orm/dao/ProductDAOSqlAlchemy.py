from sqlalchemy.orm import sessionmaker
from db.database import getConnection
from model.model import Product

class ProductDAOSqlAlchemy:
    def __init__(self):
        self.connection = getConnection()
        self.Session = sessionmaker(bind=self.connection)
        
    def GetProductByName(self, product_name):
        session = self.Session()
        try:
            product = session.query(Product).filter(Product.productname.ilike(product_name)).first()
            return product
        except Exception as e:
            print(f"Error getting product by name: {e}")
            return None
        finally:
            session.close()