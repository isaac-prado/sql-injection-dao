from sqlalchemy import func, distinct, desc
from orm.db.database import getSession
from orm.model.model import Employees, Orders, OrderDetails

class EmployeeDAOSqlAlchemy:
    def __init__(self):
        self.session = getSession()
        
    def GetEmployeeByName(self, employee_name):
        try:
            employee = self.session.query(Employees).filter(Employees.firstname.ilike(employee_name)).first()
            return employee
        except Exception as e:
            print(f"Error getting employee by name: {e}")
            return None
        
    def GetEmployeeRanking(self, initial_date, final_date):
        try:
            ranking = self.session.query(
                (Employees.firstname + " " + Employees.lastname.label("employee_name")),
                func.count(distinct(Orders.orderid)).label("orders_count"),
                func.sum(OrderDetails.quantity * (OrderDetails.unitprice * (1 - OrderDetails.discount))).label("total_sales")
            ).select_from(Orders
            ).join(Employees, Orders.employeeid == Employees.employeeid
            ).join(OrderDetails, Orders.orderid == OrderDetails.orderid
            ).filter(Orders.orderdate.between(initial_date, final_date)
            ).group_by(Employees.employeeid
            ).order_by(desc("total_sales")
            ).limit(5)

            return ranking.all()
        except Exception as e:
            print(f"Error getting employee ranking: {e}")
            return None
