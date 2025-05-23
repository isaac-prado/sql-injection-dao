from sqlalchemy import func
from orm.db.database import getSession
from orm.model.model import Orders, OrderDetails, Customers, Employees, Products

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
        items
    ):
        try:
            next_order_id = self.session.query(func.max(Orders.orderid)).scalar() + 1

            new_order = Orders(
                orderid=next_order_id,
                customerid=customer_id,
                employeeid=employee_id,
                orderdate=order_date,
                requireddate=required_date
            )
            self.session.add(new_order)
            self.session.flush()  # Flush to get the order_id
            
            for item in items:
                order_detail = OrderDetails(
                    orderid=next_order_id,
                    productid=item['product_id'],
                    unitprice=item['unit_price'],
                    quantity=item['quantity'],
                    discount=item['discount']
                )
                self.session.add(order_detail)

            self.session.commit()
            return next_order_id
        except Exception as e:
            print(f"Error inserting order: {e}")
            self.session.rollback()
            return None
        
    def OrderInformationById(self, order_id):
        try:
            query = self.session.query(
                Orders.orderid,
                Orders.orderdate,
                Customers.companyname.label('customer_name'),
                func.concat(Employees.firstname, ' ', Employees.lastname).label('employee_name'),
                Products.productname.label('product_name'),
                OrderDetails.quantity,
                OrderDetails.unitprice
            ).join(
                Customers, Orders.customerid == Customers.customerid
            ).join(
                Employees, Orders.employeeid == Employees.employeeid
            ).join(
                OrderDetails, Orders.orderid == OrderDetails.orderid
            ).join(
                Products, OrderDetails.productid == Products.productid
            ).filter(
                Orders.orderid == order_id
            ).all()

            return query
        except Exception as e:
            print(f"Error getting order by id: {e}")
            return None