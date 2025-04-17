from noorm.db.database import getConnection

class ProductDAO:
    def __init__(self):
        self.connection = getConnection()
        self.session = self.connection.cursor()
        
    def GetProductByName(self, product_name):
        try:
            self.session.execute("SELECT * FROM northwind.products WHERE productname ILIKE %s", (product_name,))
            row = self.session.fetchone()
            if not row:
                return None
            return {
                "productid": row[0],
                "productname": row[1],
                "supplierid": row[2],
                "categoryid": row[3],
                "quantityperunit": row[4],
                "unitprice": row[5],
                "unitsinstock": row[6],
                "unitsonorder": row[7],
                "reorderlevel": row[8],
                "discontinued": row[9]
            }
        except Exception as e:
            print(f"Error getting product by name: {e}")
            return None