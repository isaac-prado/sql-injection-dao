from db.database import getSession
from model.model import Customer

class CustomerDAOSqlAlchemy:
    def __init__(self):
        self.session = getSession()
        
    def GetCustomerByName(self, customer_name):
        try:
            customer = self.session.query(Customer).filter(Customer.companyname.ilike(f"%{customer_name}%")).first()
            return customer
        except Exception as e:
            print(f"Error getting customer by name: {e}")
            return None