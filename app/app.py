from flask import request, jsonify, g
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import exc
from cerberus import Validator

from init import create_app
from models import (
    Client,
    Service,
    Material,
    User,
    Orders,
    Address,
    EvaluationVisits,
    OrderServices,
    ServiceMaterials,
)
import database
import exceptions

app = create_app()
auth = HTTPBasicAuth()


@app.route('/', methods=['GET'])
def check():
    return "Hello World"


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token, app)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/login', methods=['POST'])
@auth.login_required
def login():
    token = g.user.generate_auth_token(app)
    return jsonify({'token': token.decode('ascii')}), 200


# USER

@app.route('/user', methods=['GET'])
@auth.login_required
def list_user():
    users = database.get_all(User)
    users_response = []
    for user in users:
        user_order = []

        for order in user.orders:
            user_order.append({
                'id': order.id,
                'client_id': order.client_id,
                'client': {
                    'id': order.client.id,
                    'full_name': order.client.full_name,
                    'email': order.client.email,
                    'phone': order.client.phone,
                    'cnpj': order.client.cnpj,
                    'cpf': order.client.cpf
                },
                'orderStatus_id': order.orderStatus_id,
                'orderStatus': {
                    'id': order.orderStatus.id,
                    'status': order.orderStatus.status,
                    'description': order.orderStatus.description
                },
                'description': order.description,
                'created_at': order.created_at,
                'updated_at': order.updated_at
            })

        user_dict = {
            'id': user.id,
            'full_name': user.full_name,
            'username': user.username,
            'email': user.email,
            'orders': user_order,
        }
        users_response.append(user_dict)

    return jsonify(users_response), 200


@app.route('/user', methods=['POST'])
def add_user():
    request_data = request.get_json()
    schema = {
        'full_name': {
            'type': 'string',
            'maxlength': 200
        },
        'username': {
            'type': 'string',
            'maxlength': 65
        },
        'password': {
            'type': 'string',
            'maxlength': 20
        },
        'email': {
            'type': 'string',
            'maxlength': 65
        }
    }

    v = Validator(require_all=True)

    if (not v.validate(request_data, schema)):
        return jsonify(v.errors), 422

    try:
        user = User(**request_data)

        user.hash_password(request_data["password"])

        database.add_instance(user)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "User already registred"}), 409


@app.route('/user/<int:id>', methods=['PUT'])
@auth.login_required
def update_user(id: int):
    request_data = request.get_json()
    schema = {
        'full_name': {
            'type': 'string',
            'maxlength': 200
        },
        'username': {
            'type': 'string',
            'maxlength': 65
        },
        'email': {
            'type': 'string',
            'maxlength': 65
        }
    }

    v = Validator()

    if (not v.validate(request_data, schema)):
        return jsonify(v.errors), 422

    try:
        if request_data["password"]:
            del request_data["password"]

        database.update_instance(User,
                                 id,
                                 **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "User already registred"}), 409
    except exceptions.NotFoundException:
        return jsonify({'error': 'User not found'}), 404


@app.route('/user/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_user(id: int):
    try:
        database.delete_instance(User, id)

        return jsonify("success"), 200
    except exceptions.NotFoundException:
        return jsonify({'error': 'User not found'}), 404


# CLIENT

@app.route('/client', methods=['GET'])
@auth.login_required
def list_clients():
    clients = database.get_all(Client)
    clients_response = []
    for client in clients:
        client_order = []

        for order in client.orders:            
            client_order.append({
                    'id': order.id,
                    'user_id': order.user_id,
                    'user': {
                        'id': order.user.id,
                        'full_name': order.user.full_name,
                        'username': order.user.username,
                        'email': order.user.email
                    },
                    'orderStatus_id': order.orderStatus_id,
                    'orderStatus': {
                        'id': order.orderStatus.id,
                        'status': order.orderStatus.status,
                        'description': order.orderStatus.description
                    },
                    'description': order.description,
                    'created_at': order.created_at,
                    'updated_at': order.updated_at
                })

        client_dict = {
            'id': client.id,
            'full_name': client.full_name,
            'email': client.email,
            'phone': client.phone,
            'cnpj': client.cnpj,
            'cpf': client.cpf,
            'orders': client_order
        }
        clients_response.append(client_dict)

    return jsonify(clients_response), 200


@app.route('/client', methods=['POST'])
@auth.login_required
def add_client():
    request_data = request.get_json()
    schema = {
        'full_name': {
            'type': 'string',
            'maxlength': 200
        },
        'email': {
            'type': 'string',
            'maxlength': 65
        },
        'phone': {
            'type': 'string',
            'minlength': 10,
            'maxlength': 11
        },
        'cnpj': {
            'type': 'string',
            'minlength': 11,
            'maxlength': 11,
            'required': False
        },
        'cpf': {
            'type': 'string',
            'minlength': 11,
            'maxlength': 11,
            'required': False
        }
    }

    v = Validator()

    if (not v.validate(request_data, schema)):
        return jsonify(v.errors), 422

    try:
        database.add_instance(Client,
                              **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "Client already registred"}), 409


@app.route('/client/<int:id>', methods=['PUT'])
@auth.login_required
def update_client(id: int):
    request_data = request.get_json()
    schema = {
        'full_name': {
            'type': 'string',
            'maxlength': 200
        },
        'email': {
            'type': 'string',
            'maxlength': 65
        },
        'phone': {
            'type': 'string',
            'minlength': 10,
            'maxlength': 11
        },
        'cnpj': {
            'type': 'string',
            'minlength': 11,
            'maxlength': 11
        },
        'cpf': {
            'type': 'string',
            'minlength': 11,
            'maxlength': 11
        }
    }

    v = Validator()

    if (not v.validate(request_data, schema)):
        return jsonify(v.errors), 422

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
@auth.login_required
def delete_client(id: int):
    try:
        database.delete_instance(Client, id)

        return jsonify("success"), 200
    except exceptions.NotFoundException:
        return jsonify({'error': 'Client not found'}), 404


# SERVICE

@app.route('/service', methods=['GET'])
@auth.login_required
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
@auth.login_required
def add_service():
    request_data = request.get_json()
    schema = {
        'name': {
            'type': 'string',
            'maxlength': 255
        },
        'description': {
            'type': 'string'
        },
        'value_hour': {
            'type': 'float'
        }
    }

    v = Validator(require_all=True)

    if (not v.validate(request_data, schema)):
        return jsonify(v.errors), 422

    try:
        database.add_instance(Service,
                              **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "Service already registred"}), 409


@app.route('/service/<int:id>', methods=['PUT'])
@auth.login_required
def update_service(id: int):
    request_data = request.get_json()
    schema = {
        'name': {
            'type': 'string',
            'maxlength': 255
        },
        'description': {
            'type': 'string'
        },
        'value_hour': {
            'type': 'float'
        }
    }

    v = Validator()

    if (not v.validate(request_data, schema)):
        return jsonify(v.errors), 422

    try:
        database.update_instance(Service,
                                 id,
                                 **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "Service already registred"}), 409


@app.route('/service/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_service(id: int):
    database.delete_instance(Service, id)

    return jsonify("success"), 200


# MATERIAL

@app.route('/material', methods=['GET'])
@auth.login_required
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
@auth.login_required
def add_material():
    request_data = request.get_json()
    schema = {
        'name': {
            'type': 'string',
            'maxlength': 255
        },
        'description': {
            'type': 'string'
        },
        'storage': {
            'type': 'integer'
        },
        'unique_value': {
            'type': 'float'
        }
    }

    v = Validator(require_all=True)

    if (not v.validate(request_data, schema)):
        return jsonify(v.errors), 422

    try:
        database.add_instance(Material,
                              **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "Material already registred"}), 409


@app.route('/material/<int:id>', methods=['PUT'])
@auth.login_required
def update_material(id: int):
    request_data = request.get_json()
    schema = {
        'name': {
            'type': 'string',
            'maxlength': 255
        },
        'description': {
            'type': 'string'
        },
        'new_items': {
            'type': 'integer'
        },
        'unique_value': {
            'type': 'float'
        }
    }

    v = Validator()

    if (not v.validate(request_data, schema)):
        return jsonify(v.errors), 422

    try:
        material = Material.query.get(id)

        if request_data['new_items'] and material is not None:
            material.storage += request_data['new_items']

        database.update_instance(material or Material,
                                 **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "Material already registred"}), 409


@app.route('/material/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_material(id: int):
    database.delete_instance(Material, id)

    return jsonify("success"), 200


# ORDER

@app.route('/order', methods=['GET'])
@auth.login_required
def list_orders():
    orders = database.get_all(Orders)
    orders_response = []
    for order in orders:
        orderAddresses_addresses = []

        for orderAddresses in order.orderAddresses:            
            orderAddresses_addresses.append({
                'id': orderAddresses.address.id,
                'cep': orderAddresses.address.cep,
                'street': orderAddresses.address.street,
                'number': orderAddresses.address.number,
                'complement': orderAddresses.address.complement,
                'city': orderAddresses.address.city,
            })

        order_dict = {
            'id': order.id,
            'client_id': order.client_id,
            'client': {
                'id': order.client.id,
                'full_name': order.client.full_name,
                'email': order.client.email,
                'phone': order.client.phone,
                'cnpj': order.client.cnpj,
                'cpf': order.client.cpf
            },
            'user_id': order.user_id,
            'user': {
                'id': order.user.id,
                'full_name': order.user.full_name,
                'username': order.user.username,
                'email': order.user.email
            },
            'orderStatus_id': order.orderStatus_id,
            'orderStatus': {
                'id': order.orderStatus.id,
                'status': order.orderStatus.status,
                'description': order.orderStatus.description
            },
            'description': order.description,
            'created_at': order.created_at,
            'updated_at': order.updated_at,
            'address': orderAddresses_addresses
        }
        orders_response.append(order_dict)

    return jsonify(orders_response), 200


@app.route('/order', methods=['POST'])
@auth.login_required
def add_order():
    request_data = request.get_json()

    try:
        database.add_instance(Orders,
                              **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "Orders already registred"}), 409


@app.route('/order/<int:id>', methods=['PUT'])
@auth.login_required
def update_order(id: int):
    request_data = request.get_json()
    try:
        database.update_instance(Orders,
                                 id,
                                 **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "Orders already registred"}), 409


@app.route('/order/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_order(id: int):
    database.delete_instance(Orders, id)

    return jsonify("success"), 200


# ADDRESS

@app.route('/address', methods=['GET'])
@auth.login_required
def list_addresses():
    addresses = database.get_all(Address)
    addresses_response = []
    for address in addresses:
        orderAddresses_orders = []

        for orderAddresses in address.orderAddresses:            
            orderAddresses_orders.append({
                'id': orderAddresses.order.id,
                'client_id': orderAddresses.order.client_id,
                'user_id': orderAddresses.order.user_id,
                'description': orderAddresses.order.description,
                'orderStatus_id': orderAddresses.order.orderStatus_id,
                'created_at': orderAddresses.order.created_at,
                'updated_at': orderAddresses.order.updated_at
            })

        address_dict = {
            'id': address.id,
            'cep': address.cep,
            'street': address.street,
            'number': address.number,
            'complement': address.complement,
            'city': address.city,
            'orders': orderAddresses_orders
        }
        addresses_response.append(address_dict)

    return jsonify(addresses_response), 200


@app.route('/address', methods=['POST'])
@auth.login_required
def add_address():
    request_data = request.get_json()

    try:
        database.add_instance(Address,
                              **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "Address already registred"}), 409


@app.route('/address/<int:id>', methods=['PUT'])
@auth.login_required
def update_address(id: int):
    request_data = request.get_json()
    try:
        database.update_instance(Address,
                                 id,
                                 **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "Address already registred"}), 409


@app.route('/address/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_address(id: int):
    database.delete_instance(Address, id)

    return jsonify("success"), 200


# EVALUATION VISITS

@app.route('/evaluationVisit', methods=['GET'])
@auth.login_required
def list_evaluationVisits():
    evaluationVisits = database.get_all(EvaluationVisits)
    evaluationVisits_response = []
    for evaluationVisit in evaluationVisits:
        evaluationVisit_dict = {
            'id': evaluationVisit.id,
            'order_id': evaluationVisit.order_id,
            'order': {
                'id': evaluationVisit.order.id,
                'client_id': evaluationVisit.order.client_id,
                'user_id': evaluationVisit.order.user_id,
                'description': evaluationVisit.order.description,
                'orderStatus_id': evaluationVisit.order.orderStatus_id,
                'created_at': evaluationVisit.order.created_at,
                'updated_at': evaluationVisit.order.updated_at,
            },
            'status_id': evaluationVisit.status_id,
            'status': {
                'id': evaluationVisit.visitStatus.id,
                'status': evaluationVisit.visitStatus.status,
                'description': evaluationVisit.visitStatus.description
            },
            'evaluation': evaluationVisit.evaluation,
            'visit_at': evaluationVisit.visit_at,
            'payment': evaluationVisit.payment
        }
        evaluationVisits_response.append(evaluationVisit_dict)

    return jsonify(evaluationVisits_response), 200


@app.route('/evaluationVisit', methods=['POST'])
@auth.login_required
def add_evaluationVisit():
    request_data = request.get_json()

    try:
        database.add_instance(EvaluationVisits,
                              **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "EvaluationVisits already registred"}), 409


@app.route('/evaluationVisit/<int:id>', methods=['PUT'])
@auth.login_required
def update_evaluationVisit(id: int):
    request_data = request.get_json()
    try:
        database.update_instance(EvaluationVisits,
                                 id,
                                 **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "EvaluationVisits already registred"}), 409


@app.route('/evaluationVisit/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_evaluationVisit(id: int):
    database.delete_instance(EvaluationVisits, id)

    return jsonify("success"), 200


# ORDER SERVICES

@app.route('/orderService', methods=['GET'])
@auth.login_required
def list_orderServices():
    orderServices = database.get_all(OrderServices)
    orderServices_response = []
    for orderService in orderServices:
        serviceMaterials_materials = []

        for serviceMaterial in orderService.serviceMaterials:            
            serviceMaterials_materials.append({
                'id': serviceMaterial.id,
                'qtd': serviceMaterial.qtd,
                'unique_value': serviceMaterial.unique_value,
                'material_id': serviceMaterial.material_id,
                'material': {
                    'id': serviceMaterial.material.id,
                    'name': serviceMaterial.material.name,
                    'description': serviceMaterial.material.description,
                    'storage': serviceMaterial.material.storage,
                    'unique_value': serviceMaterial.material.unique_value
                }
            })

        orderService_dict = {
            'id': orderService.id,
            'service_id': orderService.service_id,
            'service': {
                'id': orderService.service.id,
                'name': orderService.service.name,
                'description': orderService.service.description,
                'value_hour': orderService.service.value_hour
            },
            'order_id': orderService.order_id,
            'order': {
                'id': orderService.order.id,
                'client_id': orderService.order.client_id,
                'user_id': orderService.order.user_id,
                'description': orderService.order.description,
                'orderStatus_id': orderService.order.orderStatus_id,
                'created_at': orderService.order.created_at,
                'updated_at': orderService.order.updated_at,
            },
            'status_id': orderService.status_id,
            'status': {
                'id': orderService.visitStatus.id,
                'status': orderService.visitStatus.status,
                'description': orderService.visitStatus.description
            },
            'service_date': orderService.service_date,
            'hours_worked': orderService.hours_worked,
            'value_hour': orderService.value_hour,
            'serviceMaterials': serviceMaterials_materials
        }
        orderServices_response.append(orderService_dict)

    return jsonify(orderServices_response), 200


@app.route('/orderService', methods=['POST'])
@auth.login_required
def add_orderService():
    request_data = request.get_json()

    try:
        database.add_instance(OrderServices,
                              **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "OrderServices already registred"}), 409


@app.route('/orderService/<int:id>', methods=['PUT'])
@auth.login_required
def update_orderService(id: int):
    request_data = request.get_json()
    try:
        database.update_instance(OrderServices,
                                 id,
                                 **request_data)

        return jsonify("success"), 200
    except exc.IntegrityError:
        return jsonify({"error": "OrderServices already registred"}), 409


@app.route('/orderService/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_orderService(id: int):
    database.delete_instance(OrderServices, id)

    return jsonify("success"), 200


app.run()