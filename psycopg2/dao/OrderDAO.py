from db.database import getConnection

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
        shipped_date,
        freight,
        ship_name,
        ship_address,
        ship_city,
        ship_region,
        ship_postal_code,
        ship_country,
        shipper_id,
        items
    ):
        try:
            self.session.execute(
                '''
                INSERT INTO northwind.orders (
                    customerid, 
                    employeeid, 
                    orderdate, 
                    requireddate, 
                    shippeddate, 
                    freight, 
                    shipname, 
                    shipaddress, 
                    shipcity, 
                    shipregion, 
                    shippostalcode, 
                    shipcountry, 
                    shipperid
                    ) 
                    VALUES 
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING orderid
                ''',
                (customer_id, employee_id, order_date, required_date, shipped_date, freight, ship_name, ship_address, ship_city, ship_region, ship_postal_code, ship_country, shipper_id)
            )
            order_id = self.session.fetchone()[0]
            
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
        except Exception as e:
            print(f"Error inserting order: {e}")
            return None
        
        