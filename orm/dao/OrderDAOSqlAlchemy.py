from sqlalchemy.orm import Session
from orm.db.database import getSession
from orm.model.model import Orders, OrderDetails

class OrderDAOSqlAlchemy:
    def __init__(self):
        self.session = getSession()

    def GetOrderById(self, order_id):
        try:
            return self.session.query(Orders).filter(Orders.orderid == order_id).first()
        except Exception as e:
            print(f"Error getting order by id: {e}")
            return None

    def GetOrderByCustomerId(self, customer_id):
        try:
            return self.session.query(Orders).filter(Orders.customerid.ilike(customer_id)).all()
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
            new_order = Orders(
                customerid=customer_id,
                employeeid=employee_id,
                orderdate=order_date,
                requireddate=required_date,
                shippeddate=shipped_date,
                freight=freight,
                shipname=ship_name,
                shipaddress=ship_address,
                shipcity=ship_city,
                shipregion=ship_region,
                shippostalcode=ship_postal_code,
                shipcountry=ship_country,
                shipperid=shipper_id
            )
            self.session.add(new_order)
            self.session.flush()  # Flush to get the order_id
            
            for item in items:
                order_detail = OrderDetails(
                    orderid=new_order.orderid,
                    productid=item['product_id'],
                    unitprice=item['unit_price'],
                    quantity=item['quantity'],
                    discount=item['discount']
                )
                self.session.add(order_detail)

            self.session.commit()
            return new_order.orderid
        except Exception as e:
            print(f"Error inserting order: {e}")
            self.session.rollback()
            return None