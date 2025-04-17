from sqlalchemy.orm import Session
from db.database import getConnection
from model.model import Employee

class EmployeeDAOSqlAlchemy:
    def __init__(self):
        self.connection = getConnection()
        
    def GetEmployeeByName(self, employee_name):
        try:
            with Session(self.connection) as session:
                employee = session.query(Employee).filter(Employee.firstname.ilike(employee_name)).first()
                return employee
        except Exception as e:
            print(f"Error getting employee by name: {e}")
            return None