from dao.OrderDAO import OrderDAO
from dao.CustomerDAO import CustomerDAO
from dao.EmployeeDAO import EmployeeDAO
from dao.ProductDAO import ProductDAO
from datetime import date

dao = OrderDAO()

cliente = CustomerDAO().GetCustomerByName("Alfreds")
vendedor = EmployeeDAO().GetEmployeeByName("Nancy")
produto = ProductDAO().GetProductByName("Chai")

order_id = dao.InsertOrder(
    customer_id=cliente[0],
    employee_id=vendedor[0],
    order_date=date.today(),
    required_date=date.today(),
    shipped_date=None,
    freight=25.0,
    ship_name="Navio Teste",
    ship_address="Rua Exemplo, 123",
    ship_city="Pouso Alegre",
    ship_region="MG",
    ship_postal_code="37550-000",
    ship_country="Brasil",
    shipper_id=1,
    items=[{
        'product_id': produto[0],
        'quantity': 2,
        'unit_price': produto[2]
    }]
)

print(f"Pedido {order_id} inserido com sucesso!")
