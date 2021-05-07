
from flask import Flask
from BaseController import BaseController

class ClientController(BaseController):

    def __init__(self, model, app: Flask):
        self.schema = {
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
        super(ClientController, self).__init__(model, app, self.schema)


    def manipulateGet(self, entities):
        clients_response = []
        for client in entities:
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

        return clients_response
        