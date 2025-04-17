from dao.EmployeeDAO import EmployeeDAO

class EmployeeController:
    def __init__(self):
        self.EmployeeDAO = EmployeeDAO()

    def GetEmployeeByName(self, name):
        employee = self.EmployeeDAO.GetEmployeeByName(name)
        if not employee:
            return ValueError("Employee not found")
        return employee