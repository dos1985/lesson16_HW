import json
from models import Users, Order, Offers
from config import db

def data_user(input_data):
    for row in input_data:
        db.session.add(
            Users(
        id=row.get('id'),
        first_name=row.get('first_name'),
        last_name=row.get('last_name'),
        email=row.get('email'),
        role=row.get('role'),
        phone=row.get('phone')
        )
        )







def data_order(input_data):
    for row in input_data:
        db.session.add(
            Order(
         id=row.get('id'),
         name=row.get('name'),
         description=row.get('description'),
         start_date=row.get('start_date'),
         end_date=row.get('end_date'),
         address=row.get('address'),
         price=row.get('price'),
         customer_id=row.get('customer_id'),
         executor_id=row.get('executor_id'),
        )
        )

def data_offers(input_data):
    for row in input_data:
        db.session.add(
            Offers(
        id=row.get('id'),
        order_id=row.get('order_id'),
        executor=row.get('executor'),
            )
    )

db.drop_all()
db.create_all()


with open('data/users.json') as file:
    data = json.load(file)
    data_user(data)

with open('data/orders.json') as file:
    data = json.load(file)
    data_order(data)

with open('data/offers.json') as file:
    data = json.load(file)
    data_offers(data)