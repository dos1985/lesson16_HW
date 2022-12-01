from config import db
from flask_sqlalchemy import SQLAlchemy, Column


class Users(db.Model):
    __tablename__ = 'user'
    id = Column(db.Integer, primary_key=True)
    first_name = Column(db.String(100))
    last_name = Column(db.String(100))
    age = Column(db.Integer)
    email = Column(db.String(100))
    role = Column(db.String(100))
    phone = Column(db.Integer(100))

    def to_dict(self):
        return {"id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "role": self.role,
                "phone": self.phone
                }

class Order(db.Model):
    __tablename__ = 'order'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(100))
    description = Column(db.String(100))
    start_date = Column(db.DateTime)
    end_date = Column(db.DateTime)
    address = Column(db.String(100))
    price = Column(db.Integer)
    customer_id = Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = Column(db.Integer, db.ForeignKey('user.id'))


    def to_dict(self):
        return {"id": self.id,
                "name": self.name,
                "description": self.description,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "address": self.address,
                "price": self.price,
                "customer_id": self.customer_id,
                "executor_id": self.executor_id,
             }


class Offers(db.Model):
    __tablename__ = 'offers'
    id = Column(db.Integer, primary_key=True)
    order_id = Column(db.Integer, db.ForeignKey('order_id'))
    executor = Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {"id": self.id,
                "order_id": self.price,
                "executor_id": self.executor_id,
             }
