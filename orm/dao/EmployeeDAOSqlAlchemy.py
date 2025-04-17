from sqlalchemy.orm import Session
from orm.db.database import getSession
from orm.model.model import Employees

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