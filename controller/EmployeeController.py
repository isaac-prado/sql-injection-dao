class EmployeeController:
    def __init__(self, employee_dao):
        self.EmployeeDAO = employee_dao

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
