class CustomerController:
    def __init__(self, customer_dao):
        self.CustomerDAO = customer_dao

    def GetCustomerByName(self, name):
        customer = self.CustomerDAO.GetCustomerByName(name)

        if not customer:
            return ValueError("Customer not found")
        return customer
