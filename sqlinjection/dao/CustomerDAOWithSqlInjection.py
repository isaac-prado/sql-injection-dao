from noorm.db.database import getConnection

class CustomerDAOWithSqlInjection:
    def __init__(self):
        self.connection = getConnection()
        self.session = self.connection.cursor()

    def getCustomerByName(self, name):
        sql = f"SELECT * FROM customers WHERE name = '{name}'"
        print(f"Executing SQL: {sql}")
        self.session.execute(sql)
        result = self.session.fetchall()
        return result
