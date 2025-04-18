from orm.db.database import getSession
from orm.model.model import Customers

class CustomerDAOSqlAlchemy:
    def __init__(self):
        self.session = getSession()
        
    def GetCustomerByName(self, customer_name):
        try:
            customer = self.session.query(Customers).filter(Customers.companyname.ilike(f"%{customer_name}%")).first()
            return customer
        except Exception as e:
            print(f"Error getting customer by name: {e}")
            return None