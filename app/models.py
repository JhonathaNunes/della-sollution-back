  
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
    value_hour = db.Column(db.Float(5,2))