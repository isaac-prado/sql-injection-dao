from db.database import getConnection

class ProductDAO:
    def __init__(self):
        self.connection = getConnection()
        self.session = self.connection.cursor()
        
    def GetProductByName(self, product_name):
        try:
            self.session.execute("SELECT * FROM northwind.products WHERE productname ILIKE %s LIMIT 1", (product_name,))
            return self.session.fetchone()
        except Exception as e:
            print(f"Error getting product by name: {e}")
            return None