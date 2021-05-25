from flask import request, jsonify
from datetime import datetime
from authenticator import auth
from BaseController import BaseController
from models import (
    OrderStatus
)

class OrderController(BaseController):

    def __init__(self, model):
        self.default_schema = {
            'description': {
                'type': 'string',
                'maxlength': 255
            },
            'address_id': {
                'type': 'integer'
            },
            'client_id': {
                'type': 'integer'
            },
            'user_id': {
                'type': 'integer'
            }
        }
        super(OrderController, self).__init__(model, self.default_schema)


    def manipulate_get(self, entities):
        orders_response = []
        for order in entities:
            order_dict = {
                'id': order.id,
                'client': {
                    'id': order.client.id,
                    'full_name': order.client.full_name,
                    'email': order.client.email,
                    'phone': order.client.phone,
                    'cnpj': order.client.cnpj,
                    'cpf': order.client.cpf
                },
                'user': {
                    'id': order.user.id,
                    'full_name': order.user.full_name,
                    'username': order.user.username,
                    'email': order.user.email
                },
                'address': {
                    'id': order.address.id,
                    'cep': order.address.cep,
                    'street': order.address.street,
                    'number': order.address.number,
                    'complement': order.address.complement,
                    'city': order.address.city
                },
                'order_status': {
                    'id': order.order_status.id,
                    'status': order.order_status.status,
                    'description': order.order_status.description
                },
                'description': order.description,
                'created_at': order.created_at,
                'updated_at': order.updated_at
            }
            orders_response.append(order_dict)

        return orders_response

    
    def manipulate_post(self, request_data):
        datetime_value = datetime.now()
        status = OrderStatus.query.filter_by(status='P').first()
        request_data['order_status_id'] = status.id
        request_data['created_at'] = datetime_value
        request_data['updated_at'] = datetime_value

    
    def manipulate_put(self, entity, request_data):
        entity.updated_at = datetime.now()
        

    @auth.login_required
    def duplicate(self):
        return jsonify([{'duplicate': 'Essa rota vai duplicar a ordem, exemplo'}]), 200


    def custom_routes(self, app, model_string):
        app.add_url_rule('/'+model_string+'/duplicate', model_string+'_duplicate', self.duplicate, methods=['GET'])
        