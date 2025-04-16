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
        print("customer_id", customer_id)
        print("employee_id", employee_id)
        print("order_date", order_date)
        print("required_date", required_date)
        print("shipped_date", shipped_date)
        print("freight", freight)
        print("ship_name", ship_name)
        print("ship_address", ship_address)
        print("ship_city", ship_city)
        print("ship_region", ship_region)
        print("ship_postal_code", ship_postal_code)
        print("ship_country", ship_country)
        print("shipper_id", shipper_id)
        print("--------------------------------")
        
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
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''',
                (order_id, customer_id, employee_id, order_date, required_date, shipped_date, freight, ship_name, ship_address, ship_city, ship_region, ship_postal_code, ship_country, shipper_id)
            )
            print("order_id", order_id)
            print("--------------------------------")
            print("items", items)
            
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
        
        