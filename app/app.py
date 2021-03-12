from flask import request, jsonify

from init import create_app
from models import Client
import database

app = create_app()


@app.route('/', methods=['GET'])
def check():
    return "Hello World"


@app.route('/client', methods=['GET'])
def list_clients():
    clients = database.get_all(Client)
    clients_response = []
    for client in clients:
        client_dict = {
            'id': client.id,
            'full_name': client.full_name,
            'email': client.email,
            'phone': client.phone,
            'cnpj': client.cnpj,
            'cpf': client.cpf,
        }
        clients_response.append(client_dict)

    return jsonify(clients_response), 200


@app.route('/client', methods=['POST'])
def add_client():
    request_data = request.get_json()
    database.add_instance(Client,
                          full_name=request_data['full_name'] if "full_name"
                          in request_data else None,
                          email=request_data['email'] if 'email'
                          in request_data else None,
                          phone=request_data['phone'] if 'phone'
                          in request_data else None,
                          cnpj=request_data['cnpj'] if 'cnpj'
                          in request_data else None,
                          cpf=request_data['cpf'] if 'cpf'
                          in request_data else None)

    return jsonify("success"), 200


@app.route('/client/<int:id>', methods=['PUT'])
def update_client(id: int):
    request_data = request.get_json()
    new_atributes = {}

    for key, new_attr in request_data.items():
        new_atributes[key] = new_attr

    database.update_instance(Client,
                             id,
                             **new_atributes)

    return jsonify("success"), 200


@app.route('/client/<int:id>', methods=['DELETE'])
def delete_client(id: int):
    database.delete_instance(Client, id)

    return jsonify("success"), 200


app.run()
