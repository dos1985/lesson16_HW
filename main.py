import json

from flask import jsonify, request
from sqlalchemy.sql.elements import and_

from config import app, db
from creat_db import init_db
from models import Users, Order, Offer

@app.route('/users/', methods=['GET', 'POST'])
def get_users():
    if request.method == 'POST':
        data = request.json
        all_users = db.session.query(Users).all()
        all_users_id = []
        for user_ in all_users:
            all_users_id.append(user_.id)
        if data.get('id') not in all_users_id:
            new_user = Users(id=data.get('id'),
                            first_name=data.get('first_name'),
                            last_name=data.get('last_name'),
                            age=data.get('age'),
                            email=data.get('email'),
                            role=data.get('role'),
                            phone=data.get('phone'))
            db.session.add(new_user)
            db.session.commit()
            db.session.close()
            return f"User {data.get('id')} created"
        else:
            return f"User with id {data.get('id')} already exists"
    elif request.method == 'GET':
        all_users = db.session.query(Users).all()
        all_users_list = []
        for user_ in all_users:
            temp_dict = {}
            temp_dict['id'] = user_.id
            temp_dict['age'] = user_.age
            temp_dict['first_name'] = user_.first_name
            temp_dict['last_name'] = user_.last_name
            temp_dict['last_name'] = user_.last_name
            temp_dict['email'] = user_.email
            temp_dict['phone'] = user_.phone
            all_users_list.append(temp_dict)
        return jsonify(all_users_list)

@app.route('/users/<int:uid>/', methods=['GET', 'PUT', 'DELETE'])
def users_id(uid):
    """одиночный пользователь. получение, изменение и удаление"""
    all_users = db.session.query(Users).filter(Users.id == uid).first()
    if all_users:
        if request.method == 'GET':
            temp_dict = {}
            temp_dict['id'] = all_users.id
            temp_dict['age'] = all_users.age
            temp_dict['first_name'] = all_users.first_name
            temp_dict['last_name'] = all_users.last_name
            temp_dict['last_name'] = all_users.last_name
            temp_dict['email'] = all_users.email
            temp_dict['phone'] = all_users.phone
            return jsonify(temp_dict)

        elif request.method == 'DELETE':
            item_del = Users.query.get(uid)
            db.session.delete(item_del)
            db.session.commit()
            db.session.close()
            return f'Item - {uid} removed from DB'
        elif request.method == 'PUT':
            item_put = Users.query.get(uid)
            new_data = request.json

            item_put.first_name = new_data.get('first_name')
            item_put.last_name = new_data.get('last_name')
            item_put.age = new_data.get('age')
            item_put.email = new_data.get('email')
            item_put.role = new_data.get('role')
            item_put.phone = new_data.get('phone')

            db.session.add(item_put)
            db.session.commit()
            db.session.close()
            return f'Item {uid} changed'

        return 'Unknown type request'
    return 'Not found'

@app.route('/orders/', methods=['GET', 'POST'])
def orders():
    all_orders = db.session.query(Order).all()
    all_orders_list = []
    for order_ in all_orders:
        temp_dict = {}
        temp_dict['id'] = order_.id
        temp_dict['name'] = order_.name
        temp_dict['address'] = order_.address
        temp_dict['price'] = order_.price
        temp_dict['customer_name'] = ''
        temp_dict['executor_name'] = ''
        if order_.customer:
            temp_dict['customer_name'] = order_.customer.first_name
        if order_.executor:
            temp_dict['executor_name'] = order_.executor.first_name
        all_orders_list.append(temp_dict)
    return jsonify(all_orders_list)


@app.route('/orders/<int:uid>/', methods=['GET', 'PUT', 'DELETE'])
def orders_id(uid):
    all_orders = db.session.query(Order).filter(Order.id == uid).one()
    if all_orders:
        if request.method == 'GET':
            temp_table = {}
            temp_table['Order_id'] = all_orders.id
            temp_table['Order_name'] = all_orders.name
            temp_table['Customer_name'] = ''
            temp_table['executor_name'] = ''
            if all_orders.customer:
                temp_table['Customer_name'] = all_orders.customer.first_name
            if all_orders.executor:
                temp_table['executor_name'] = all_orders.executor.first_name
            return jsonify(temp_table)


@app.route('/offers/', methods=['GET', 'POST'])
def offers():
    if request.method == 'POST':
        data = request.json
        all_offers = db.session.query(Offer).all()
        all_offers_id = []
        for order_ in all_offers:
            all_offers_id.append(order_.id)
        if data.get('id') not in all_offers_id:

            new_offer = Offers(id=data.get('id'),
                              order_id=data.get('order_id'),
                              executor_id=data.get('executor_id'))
            db.session.add(new_offer)
            db.session.commit()
            db.session.close()
            return f"Offer {data.get('id')} created"
        else:
            return f"Offer with id {data.get('id')} already exists"
    elif request.method == 'GET':
        all_offers = db.session.query(Offer.id, Offer.order_id, Offer.executor_id,
                                      Order.name).\
            join(Order, and_(Offer.order_id == Order.id)).all()
        all_offers_list = []
        for offer_ in all_offers:
            temp_dict = {}
            temp_dict['id'] = offer_.id
            temp_dict['order_id'] = offer_.order_id
            temp_dict['executor_id'] = offer_.executor_id
            temp_dict['name'] = offer_.name
            all_offers_list.append(temp_dict)
        return jsonify(all_offers_list)
    return 'Unknown type request'


@app.route('/offers/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def offers_id(uid):
    all_offers = db.session.query(Offer).filter(Offer.id == uid).first()
    if all_offers:
        if request.method == 'GET':
            offer_ = Offer.query.get(uid)
            temp_dict = {}
            temp_dict['id'] = offer_.id
            temp_dict['order_id'] = offer_.order_id
            if all_offers.user:
                temp_dict['executor_name'] = all_offers.user.first_name
            temp_dict['executor_id'] = offer_.executor_id
            return jsonify(temp_dict)
        elif request.method == 'DELETE':
            offer_ = Offer.query.get(uid)
            db.session.delete(offer_)
            db.session.commit()
            db.session.close()
            return f'Item {uid} removed from DB'
        elif request.method == 'PUT':
            item_put = Offer.query.get(uid)
            new_data = request.json

            item_put.id = new_data.get('id')
            item_put.order_id = new_data.get('order_id')
            item_put.executor_id = new_data.get('executor_id')

            db.session.add(item_put)
            db.session.commit()
            db.session.close()
            return f'Item {uid} changed'
    return 'Not found'

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080, debug=True)