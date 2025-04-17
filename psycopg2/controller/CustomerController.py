from dao.CustomerDAO import CustomerDAO

class CustomerController:
    def __init__(self):
        self.CustomerDAO = CustomerDAO()

    def GetCustomerByName(self, name):
        customer = self.CustomerDAO.GetCustomerByName(name)
        if not customer:
            return ValueError("Customer not found")
        return customer
