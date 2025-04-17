from noorm.db.database import getConnection

class EmployeeDAO:
    def __init__(self):
        self.connection = getConnection()
        self.session = self.connection.cursor()
        
    def GetEmployeeByName(self, employee_name):
        try:
            self.session.execute("SELECT employeeid FROM northwind.employees WHERE firstname ILIKE %s LIMIT 1", (employee_name,))
            return self.session.fetchone()
        except Exception as e:
            print(f"Error getting employee by name: {e}")
            return None