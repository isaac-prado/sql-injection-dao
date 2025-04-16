from dao.OrderDAO import OrderDAO

class OrderController:
    def __init__(self):
        self.order_dao = OrderDAO()

    def create_order(self, order):
        return self.order_dao.create_order(order)
