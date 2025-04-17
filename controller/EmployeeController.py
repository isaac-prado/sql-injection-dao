from orm.dao.EmployeeDAOSqlAlchemy import EmployeeDAOSqlAlchemy
from noorm.dao.EmployeeDAO import EmployeeDAO

class EmployeeController:
    def __init__(self, using_orm: bool):
        self.using_orm = using_orm

        if using_orm:
            self.EmployeeDAO = EmployeeDAOSqlAlchemy()
        else:
            self.EmployeeDAO = EmployeeDAO()

    def GetEmployeeByName(self, name):
        employee = self.EmployeeDAO.GetEmployeeByName(name)

        if not employee:
            return ValueError("Employee not found")
        return employee
    
    def GetEmployeeRanking(self, initial_date, final_date):
        try:
            return self.EmployeeDAO.GetEmployeeRanking(initial_date, final_date)
        except Exception as e:
            print(f"Error getting employee ranking: {e}")
            return None
