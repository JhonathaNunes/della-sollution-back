
from flask import Flask
from BaseController import BaseController

class OrderController(BaseController):

    def __init__(self, model, app: Flask):
        self.schema = {}
        super(OrderController, self).__init__(model, app, self.schema)


    def manipulateGet(self, entities):
        orders_response = []
        for order in entities:
            order_address = []

            for oa in order.order_address:
                order_address.append({
                    'id': oa.address.id,
                    'cep': oa.address.cep,
                    'street': oa.address.street,
                    'number': oa.address.number,
                    'complement': oa.address.complement,
                    'city': oa.address.city,
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
                'order_status_id': order.order_status_id,
                'order_status': {
                    'id': order.orderStatus.id,
                    'status': order.orderStatus.status,
                    'description': order.orderStatus.description
                },
                'description': order.description,
                'created_at': order.created_at,
                'updated_at': order.updated_at,
                'address': order_address
            }
            orders_response.append(order_dict)

        return orders_response
