  
from flask import Flask

from models import db, Client, Service, Material
import config


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    initial_dbdata()
    return app

def initial_dbdata():
    clients = [
        Client(full_name = 'Pedro Henrique e Davi Contábil ME', email = 'auditoria@pedrohenriqueedavicontabilme.com.br', phone = '984095092', cnpj = '97720969000179'),
        Client(full_name = 'Mateus Julio Cardoso', email = 'mateusjuliocardoso@arbitral.com', phone = '998064352', cpf = '82389060323'),
        Client(full_name = 'Hadassa e Luciana Financeira Ltda', email = 'qualidade@hadassaelucianafinanceiraltda.com.br', phone = '986741794', cnpj = '74369420000186'),
        Client(full_name = 'Sônia Débora Sophia das Neves', email = 'soniadeborasophiadasneves_@unink.com.br', phone = '997571040', cpf = '72857997183'),
        Client(full_name = 'Gustavo Victor Caldeira', email = 'gustavovictorcaldeira_@azulcargo.com.br', phone = '981339476', cpf = '57135962141')
    ]

    services = [
        Service(name = 'Serviço 1', description = 'Serviço 1', value_hour = 123.45),
        Service(name = 'Serviço 2', description = 'Serviço 2', value_hour = 678.91),
        Service(name = 'Serviço 3', description = 'Serviço 3', value_hour = 11.12),
        Service(name = 'Serviço 4', description = 'Serviço 4', value_hour = 131.14),
        Service(name = 'Serviço 5', description = 'Serviço 5', value_hour = 151.16)
    ]

    materials = [
        Material(name = 'Material 1', description = 'Material 1', storage = 53, unique_value = 1324.564),
        Material(name = 'Material 2', description = 'Material 2', storage = 14, unique_value = 321.12),
        Material(name = 'Material 3', description = 'Material 3', storage = 45, unique_value = 13.50),
        Material(name = 'Material 4', description = 'Material 4', storage = 23, unique_value = 452.32),
        Material(name = 'Material 5', description = 'Material 5', storage = 112, unique_value = 661.233)
    ]

    if Client.query.count() == 0:
        for client in clients:
            db.session.add(client)

    if Service.query.count() == 0:
        for service in services:
            db.session.add(service)

    if Material.query.count() == 0:
        for material in materials:
            db.session.add(material)

    db.session.commit()