from noorm.dao.OrderDAO import OrderDAO
from noorm.dao.CustomerDAO import CustomerDAO
from noorm.dao.EmployeeDAO import EmployeeDAO
from noorm.dao.ProductDAO import ProductDAO

from sqlinjection.dao.OrderDAOWithSqlInjection import OrderDAOWithSqlInjection

from orm.dao.OrderDAOSqlAlchemy import OrderDAOSqlAlchemy
from orm.dao.CustomerDAOSqlAlchemy import CustomerDAOSqlAlchemy
from orm.dao.EmployeeDAOSqlAlchemy import EmployeeDAOSqlAlchemy
from orm.dao.ProductDAOSqlAlchemy import ProductDAOSqlAlchemy

from controller.CustomerController import CustomerController
from controller.EmployeeController import EmployeeController
from controller.ProductController import ProductController

from typing import Dict, List
from datetime import datetime, timedelta

class OrderController:
    def __init__(self, using_orm: bool, sql_injection_enabled: bool):
        self.using_orm = using_orm

        if using_orm and sql_injection_enabled:
            raise Exception("Não é possível usar o SQLAlchemy e habilitar SQL Injection ao mesmo tempo.")

        if using_orm:
            self.order_dao = OrderDAOSqlAlchemy()
            self.customer_controller = CustomerController(CustomerDAOSqlAlchemy())
            self.employee_controller = EmployeeController(EmployeeDAOSqlAlchemy())
            self.product_controller = ProductController(ProductDAOSqlAlchemy())
            print("--------------------------------")
            print("UTILIZANDO SQLALCHEMY")
            print("--------------------------------")
        elif sql_injection_enabled:
            self.order_dao = OrderDAOWithSqlInjection()
            print("--------------------------------")
            print("⚠️ UTILIZANDO SQL INJECTION ⚠️")
            print("--------------------------------")
        else:
            self.order_dao = OrderDAO()
            self.customer_controller = CustomerController(CustomerDAO())
            self.employee_controller = EmployeeController(EmployeeDAO())
            self.product_controller = ProductController(ProductDAO())
            print("--------------------------------")
            print("UTILIZANDO PSYCOPG2 PROTEGIDO CONTRA SQL INJECTION")
            print("--------------------------------")
            
    def InsertOrder(
        self,
        customer_name: str,
        employee_name: str,
        ship_data: Dict,
        items: List[Dict]
        ):
        try:
            customer = self.customer_controller.GetCustomerByName(customer_name)
            employee = self.employee_controller.GetEmployeeByName(employee_name)
            formated_items = []

            for item in items:
                product = self.product_controller.GetProductByName(item.get("productname"))

                if not product:
                    raise ValueError("Produto não encontrado")
                
                if self.using_orm:
                    product_id = product.productid
                    unitprice = product.unitprice
                else:
                    product_id = product["productid"]
                    unitprice = product["unitprice"]
                
                formated_items. append({
                    "product_id": product_id,
                    "unit_price": unitprice,
                    "quantity": item.get("quantity"),
                    "discount": item.get("discount")
                })

                if self.using_orm:
                    customer_id = customer.customerid
                    employee_id = employee.employeeid
                else:
                    customer_id = customer["customerid"]
                    employee_id = employee["employeeid"]

                order_id = self.order_dao.InsertOrder(
                    customer_id=customer_id,
                    employee_id=employee_id,
                    order_date=datetime.now(),
                    required_date=ship_data.get("required_date", datetime.now() + timedelta(days=30)),
                    shipped_date=ship_data.get("shipped_date", None),
                    freight=ship_data.get("freight", None),
                    ship_name=ship_data.get("ship_name", None),
                    ship_address=ship_data.get("ship_address", None),
                    ship_city=ship_data.get("ship_city", None),
                    ship_region=ship_data.get("ship_region", None),
                    ship_postal_code=ship_data.get("ship_postal_code", None),
                    ship_country=ship_data.get("ship_country", None),
                    shipper_id=ship_data.get("shipper_id", None),
                    items=formated_items
                )

                print("--------------------------------")
                print("ORDER ID DO PEDIDO ENVIADO:")
                print(order_id)
                print("--------------------------------")
                return order_id
        except Exception as e:
            print(f"Error inserting order: {e}")
            raise e


            
            