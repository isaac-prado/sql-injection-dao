from noorm.db.database import getConnection

class CustomerDAOWithSqlInjection:
    def __init__(self):
        self.connection = getConnection()
        self.session = self.connection.cursor()

    def GetCustomerByName(self, name):
        sql = f"SELECT * FROM northwind.customers WHERE companyname = '{name}'"
        print(f"Executing SQL: {sql}")
        self.session.execute(sql)
        result = self.connection.commit()
        return result
