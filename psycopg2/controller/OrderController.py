from dao.OrderDAO import OrderDAO
from controller.CustomerController import CustomerController
from controller.EmployeeController import EmployeeController
from controller.ProductController import ProductController

from typing import Dict, List
from datetime import datetime, timedelta

class OrderController:
    def __init__(self):
        self.order_dao = OrderDAO()
        self.customer_controller = CustomerController()
        self.employee_controller = EmployeeController()
        self.product_controller = ProductController()
        
    def InsertOrder(
        self,
        customer_id: str,
        employee_id: str,
        ship_data: Dict,
        items: List[Dict]
        ):
        try:
            customer = self.customer_controller.GetCustomerByName(customer_id)
            employee = self.employee_controller.GetEmployeeByName(employee_id)

            formated_items = []
            for item in items:
                product = self.product_controller.GetProductByName(item["productname"])

                discount = product.get("discount")
                if not (0 <= discount <= 1):
                    raise ValueError("Discount must be between 0 and 1")
                
                formated_items.append({
                    "productid": product.get("productid"),
                    "unitprice": product.get("unitprice"),
                    "quantity": item.get("quantity"),
                    "discount": discount
                })

                order_id = self.order_dao.InsertOrder(
                    customer_id=customer.customerid,
                    employee_id=employee.employeeid,
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

                return order_id
        except Exception as e:
            print(f"Error inserting order: {e}")
            raise e


            
            