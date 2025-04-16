from db.database import getConnection

class ProductDAO:
    def __init__(self):
        self.connection = getConnection()
        self.session = self.connection.cursor()
        
    def GetProductById(self, product_id):
        try:
            self.session.execute("SELECT * FROM northwind.products WHERE productid = %s", (product_id,))
            return self.session.fetchone()
        except Exception as e:
            print(f"Error getting product by id: {e}")
            return None
        
    def GetProductByName(self, product_name):
        try:
            self.session.execute("SELECT * FROM northwind.products WHERE productname ILIKE %s", (product_name,))
            return self.session.fetchall()
        except Exception as e:
            print(f"Error getting product by name: {e}")