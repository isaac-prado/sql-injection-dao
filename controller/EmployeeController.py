class EmployeeController:
    def __init__(self, employee_dao):
        self.EmployeeDAO = employee_dao

    def GetEmployeeByName(self, name):
        employee = self.EmployeeDAO.GetEmployeeByName(name)
        if not employee or not getattr(employee, "employeeid", None):
            return ValueError("Employee not found")
        return employee