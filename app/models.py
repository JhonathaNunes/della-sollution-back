  
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200))
    email = db.Column(db.String(250), unique=True)
    phone = db.Column(db.String(11))
    cnpj = db.Column(db.String(14))
    cpf = db.Column(db.String(14), unique=True)


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(2000))
    value_hour = db.Column(db.Float(precision='5,2'))


class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(2000))
    storage = db.Column(db.Integer)
    unique_value = db.Column(db.Float(precision='8,3'))


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200))
    user_name = db.Column(db.String(65), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(65), unique=True)


class Order_Status(db.Model):
    __tablename__ = 'order_status'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(250), unique=True)
    description = db.Column(db.String(250))


class Visit_Status(db.Model):
    __tablename__ = 'visit_status'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(250), unique=True)
    description = db.Column(db.String(250))
