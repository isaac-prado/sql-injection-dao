from noorm.db.database import getConnection

class OrderDAOWithSqlInjection:
    def __init__(self):
        self.connection = getConnection()
        self.session = self.connection.cursor()

    def GetOrderById(self, order_id):
        try:
            query = f"SELECT * FROM northwind.orders WHERE orderid = {order_id}"
            print("[⚠️ QUERY VULNERÁVEL ⚠️] ", query)
            self.session.execute(query)
            return self.session.fetchone()
        except Exception as e:
            print(f"Error getting order by id: {e}")
            return None

    def GetOrderByCustomerId(self, customer_id):
        try:
            query = f"SELECT * FROM northwind.orders WHERE customerid ILIKE '{customer_id}'"
            print("[⚠️ QUERY VULNERÁVEL ⚠️] ", query)
            self.session.execute(query)
            return self.session.fetchall()
        except Exception as e:
            print(f"Error getting order by customer id: {e}")
            return None
        
    def InsertOrder(
        self,
        customer_id, 
        employee_id,
        order_date,
        required_date,
        items
    ):
        try:
            self.session.execute("SELECT MAX(orderid) + 1 FROM northwind.orders")
            order_id = self.session.fetchone()[0]

            insert_order = f"""
                INSERT INTO northwind.orders (
                    orderid, 
                    customerid, 
                    employeeid, 
                    orderdate, 
                    requireddate
                ) VALUES (
                    {order_id}, '{customer_id}', {employee_id}, '{order_date}', '{required_date}'
                )
            """
            print(f"[⚠️ QUERY VULNERÁVEL ⚠️] Executando: {insert_order}")
            self.session.execute(insert_order)
            
            for item in items:
                insert_order_details = f"""
                    INSERT INTO northwind.order_details (
                        orderid, productid, unitprice, quantity, discount
                    ) VALUES (
                        {order_id}, {item['product_id']}, {item['unit_price']}, {item['quantity']}, {item['discount']}
                    )
                """
                print(f"[⚠️ QUERY VULNERÁVEL ⚠️] Executando: {insert_order_details}")
                self.session.execute(insert_order_details)

            self.connection.commit()
            return order_id
        except Exception as e:
            print(f"Error inserting order: {e}")
            return None
        
        