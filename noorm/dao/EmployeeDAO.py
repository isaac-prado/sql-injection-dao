from noorm.db.database import getConnection

class EmployeeDAO:
    def __init__(self):
        self.connection = getConnection()
        self.session = self.connection.cursor()
        
    def GetEmployeeByName(self, employee_name):
        try:
            self.session.execute("SELECT employeeid FROM northwind.employees WHERE firstname ILIKE %s LIMIT 1", (employee_name,))
            row = self.session.fetchone()
            if not row:
                return None
            return { "employeeid": row[0] }
        except Exception as e:
            print(f"Error getting employee by name: {e}")

    def GetEmployeeRanking(self, initial_date, final_date):
        try:
            query = """
                SELECT 
                    e.firstname || ' ' || e.lastname AS employee_name,
                    COUNT(DISTINCT o.orderid) AS orders_count,
                    SUM(od.quantity * (od.unitprice * (1 - od.discount))) AS total_sales
                FROM northwind.orders o
                JOIN northwind.employees e ON o.employeeid = e.employeeid
                JOIN northwind.order_details od ON o.orderid = od.orderid
                WHERE o.orderdate BETWEEN %s AND %s
                GROUP BY e.employeeid
                ORDER BY total_sales DESC
                LIMIT 5
            """
            self.session.execute(query, (initial_date, final_date))
            return self.session.fetchall()
        
        except Exception as e:
            print(f"Error getting employee ranking: {e}")
            return None
            