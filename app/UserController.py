
from flask import Flask
from BaseController import BaseController

class UserController(BaseController):

    def __init__(self, model, app: Flask):
        self.schema = {
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
        super(UserController, self).__init__(model, app, self.schema)


    def manipulateGet(self, entities):
        users_response = []
        for user in entities:
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

        return users_response


    def manipulatePost(self, entity, request_data):
        entity.hash_password(request_data["password"])


    def manipulatePut(self, entity, request_data):
        if request_data["password"]:
            del request_data["password"]
            