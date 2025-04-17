from sqlalchemy.orm import Session
from orm.db.database import getConnection
from orm.model.model import Employees

class EmployeeDAOSqlAlchemy:
    def __init__(self):
        self.connection = getConnection()
        
    def GetEmployeeByName(self, employee_name):
        try:
            with Session(self.connection) as session:
                employee = session.query(Employees).filter(Employees.firstname.ilike(employee_name)).first()
                return employee
        except Exception as e:
            print(f"Error getting employee by name: {e}")
            return None