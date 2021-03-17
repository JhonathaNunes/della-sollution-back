from flask import request, jsonify
from sqlalchemy import exc

from init import create_app
from models import Client, Service, Material
import database
import exceptions

app = create_app()


@app.route('/', methods=['GET'])
def check():
    return "Hello World"

# CLIENT

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

    try:
        database.add_instance(Client,
                              **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "Client already registred"}), 409


@app.route('/client/<int:id>', methods=['PUT'])
def update_client(id: int):
    request_data = request.get_json()
    try:
        database.update_instance(Client,
                                 id,
                                 **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "Client already registred"}), 409
    except exceptions.NotFoundException:
        return jsonify({'error': 'Client not found'}), 404



@app.route('/client/<int:id>', methods=['DELETE'])
def delete_client(id: int):
    try:
        database.delete_instance(Client, id)

        return jsonify("success"), 200
    except exceptions.NotFoundException:
        return jsonify({'error': 'Client not found'}), 404

# SERVICE

@app.route('/service', methods=['GET'])
def list_services():
    services = database.get_all(Service)
    services_response = []
    for service in services:
        service_dict = {
            'id': service.id,
            'name': service.name,
            'description': service.description,
            'value_hour': "{:.2f}".format(service.value_hour).rstrip('0')
        }
        services_response.append(service_dict)

    return jsonify(services_response), 200


@app.route('/service', methods=['POST'])
def add_service():
    request_data = request.get_json()

    try:
        database.add_instance(Service,
                              **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "Service already registred"}), 409


@app.route('/service/<int:id>', methods=['PUT'])
def update_service(id: int):
    request_data = request.get_json()
    try:
        database.update_instance(Service,
                                 id,
                                 **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "Service already registred"}), 409



@app.route('/service/<int:id>', methods=['DELETE'])
def delete_service(id: int):
    database.delete_instance(Service, id)

    return jsonify("success"), 200


# MATERIAL

@app.route('/material', methods=['GET'])
def list_materials():
    materials = database.get_all(Material)
    materials_response = []
    for material in materials:
        materials_dict = {
            'id': material.id,
            'name': material.name,
            'description': material.description,
            'storage': material.storage,
            'unique_value': "{:.3f}".format(material.unique_value).rstrip('0')
        }
        materials_response.append(materials_dict)

    return jsonify(materials_response), 200


@app.route('/material', methods=['POST'])
def add_material():
    request_data = request.get_json()

    try:
        database.add_instance(Material,
                              **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "Material already registred"}), 409


@app.route('/material/<int:id>', methods=['PUT'])
def update_material(id: int):
    request_data = request.get_json()
    try:
        database.update_instance(Material,
                                 id,
                                 **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "Material already registred"}), 409



@app.route('/material/<int:id>', methods=['DELETE'])
def delete_material(id: int):
    database.delete_instance(Material, id)

    return jsonify("success"), 200


app.run()
