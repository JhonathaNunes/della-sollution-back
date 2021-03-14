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
                          **request_data)

    return jsonify("success"), 200


@app.route('/client/<int:id>', methods=['PUT'])
def update_client(id: int):
    request_data = request.get_json()
    database.update_instance(Client,
                             id,
                             **request_data)

    return jsonify("success"), 200


@app.route('/client/<int:id>', methods=['DELETE'])
def delete_client(id: int):
    database.delete_instance(Client, id)

    return jsonify("success"), 200


app.run()
