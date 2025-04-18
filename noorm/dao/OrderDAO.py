from noorm.db.database import getConnection

class OrderDAO:
    def __init__(self):
        self.connection = getConnection()
        self.session = self.connection.cursor()

    def GetOrderById(self, order_id):
        try:
            self.session.execute("SELECT * FROM northwind.orders WHERE orderid = %s", (order_id,))
            return self.session.fetchone()
        except Exception as e:
            print(f"Error getting order by id: {e}")
            return None

    def GetOrderByCustomerId(self, customer_id):
        try:
            self.session.execute("SELECT * FROM northwind.orders WHERE customerid ILIKE %s", (customer_id,))
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
            # NO AUTO-INCREMENT
            self.session.execute(
                '''
                SELECT MAX(orderid) + 1 FROM northwind.orders
                '''
            )
            order_id = self.session.fetchone()[0]

            self.session.execute(
                '''
                INSERT INTO northwind.orders (
                    orderid,
                    customerid, 
                    employeeid, 
                    orderdate, 
                    requireddate
                    ) 
                    VALUES 
                    (%s, %s, %s, %s, %s)
                ''',
                (order_id, customer_id, employee_id, order_date, required_date)
            )
            
            for item in items:
                self.session.execute(
                    '''
                    INSERT INTO northwind.order_details (
                        orderid, 
                        productid, 
                        unitprice, 
                        quantity, 
                        discount
                    )
                    VALUES
                    (%s, %s, %s, %s, %s)
                    ''',
                    (order_id, item['product_id'], item['unit_price'], item['quantity'], item['discount'])
                )

            self.connection.commit()
            return order_id
        except Exception as e:
            print(f"Error inserting order: {e}")
            return None
        
    def OrderInformationById(self, order_id):
        try:
            query = """
                SELECT 
                    o.orderid,
                    o.orderdate,
                    c.companyname AS customer_name,
                    e.firstname || ' ' || e.lastname AS employee_name,
                    p.productname,
                    od.quantity,
                    od.unitprice
                FROM northwind.orders o
                JOIN northwind.customers c ON o.customerid = c.customerid
                JOIN northwind.employees e ON o.employeeid = e.employeeid
                JOIN northwind.order_details od ON o.orderid = od.orderid
                JOIN northwind.products p ON od.productid = p.productid
                WHERE o.orderid = %s
            """

            self.session.execute(query, (order_id,))
            return self.session.fetchall()
        except Exception as e:
            print(f"Error getting order by id: {e}")
            return None