from db.database import getConnection

class CustomerDAO:
    def __init__(self):
        self.connection = getConnection()
        self.session = self.connection.cursor()
        
    def GetCustomerByName(self, customer_name):
        try:
            self.session.execute("SELECT customerid FROM northwind.customers WHERE companyname ILIKE %s", (customer_name,))
            return self.session.fetchone()
        except Exception as e:
            print(f"Error getting customer by name: {e}")
            return None