from BaseController import BaseController

class ClientController(BaseController):

    def __init__(self, model):
        self.default_schema = {
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
                'minlength': 14,
                'maxlength': 14,
                'required': False
            },
            'cpf': {
                'type': 'string',
                'minlength': 11,
                'maxlength': 11,
                'required': False
            }
        }
        super(ClientController, self).__init__(model, self.default_schema)


    def manipulate_get(self, entities):
        clients_response = []
        for client in entities:
            client_dict = {
                'id': client.id,
                'full_name': client.full_name,
                'email': client.email,
                'phone': client.phone,
                'cnpj': client.cnpj,
                'cpf': client.cpf
            }
            clients_response.append(client_dict)

        return clients_response
        