from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import time
import jwt

db = SQLAlchemy()


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200))
    email = db.Column(db.String(250), unique=True)
    phone = db.Column(db.String(11))
    cnpj = db.Column(db.String(14))
    cpf = db.Column(db.String(14), unique=True)
    orders = db.relationship('Orders', backref='client', lazy=True)


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    value_hour = db.Column(db.Float(precision='5,2'))
    orderServices = db.relationship('OrderServices', backref='service', lazy=True)


class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    storage = db.Column(db.Integer)
    unique_value = db.Column(db.Float(precision='8,3'))
    serviceMaterials = db.relationship('ServiceMaterials', backref='material', lazy=True)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200))
    username = db.Column(db.String(65), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(65), unique=True)
    orders = db.relationship('Orders', backref='user', lazy=True)

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, app, expires_in=86400):
        return jwt.encode(
            {'id': self.id, 'exp': time.time() + expires_in},
            app.config['SECRET_KEY'],
            algorithm='HS256')

    @staticmethod
    def verify_auth_token(token, app):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except Exception:
            return

        return User.query.get(data['id'])


class OrderStatus(db.Model):
    __tablename__ = 'order_status'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(250), unique=True)
    description = db.Column(db.Text)
    orders = db.relationship('Orders', backref='orderStatus', lazy=True)


class VisitStatus(db.Model):
    __tablename__ = 'visit_status'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(250), unique=True)
    description = db.Column(db.Text)
    evaluationVisits = db.relationship('EvaluationVisits', backref='visitStatus', lazy=True)
    orderServices = db.relationship('OrderServices', backref='visitStatus', lazy=True)


class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    cep = db.Column(db.Integer)
    street = db.Column(db.String(255))
    number = db.Column(db.Integer)
    complement = db.Column(db.String(50))
    city = db.Column(db.String(70))
    orderAddresses = db.relationship('OrderAddresses', backref='address', lazy=True)


class EvaluationVisits(db.Model):
    __tablename__ = 'evaluation_visits'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('visit_status.id'))
    evaluation = db.Column(db.Text)
    visit_at = db.Column(db.DateTime)
    payment = db.Column(db.Float(precision='8,3'))


class ServiceMaterials(db.Model):
    __tablename__ = 'service_materials'
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'))
    orderService_id = db.Column(db.Integer, db.ForeignKey('order_services.id'))
    qtd = db.Column(db.Integer)
    unique_value = db.Column(db.Float(precision='8,3'))


class OrderServices(db.Model):
    __tablename__ = 'order_services'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('visit_status.id'))
    service_date = db.Column(db.DateTime)
    hours_worked = db.Column(db.Float(precision='5,2'))
    value_hour = db.Column(db.Float(precision='5,2'))
    serviceMaterials = db.relationship('ServiceMaterials', backref='orderService', lazy=True)


class OrderAddresses(db.Model):
    __tablename__ = 'order_addresses'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))


class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    orderStatus_id = db.Column(db.Integer, db.ForeignKey('order_status.id'))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    orderAddresses = db.relationship('OrderAddresses', backref='order', lazy=True)
    evaluationVisits = db.relationship('EvaluationVisits', backref='order', lazy=True)
    orderServices = db.relationship('OrderServices', backref='order', lazy=True)
