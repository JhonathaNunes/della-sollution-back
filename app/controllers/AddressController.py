from BaseController import BaseController

class AddressController(BaseController):

    def __init__(self, model):
        self.default_schema = {
            'cep': {
                'type': 'string',
                'maxlength': 9
            },
            'street': {
                'type': 'string',
                'maxlength': 255
            },
            'number': {
                'type': 'integer'
            },
            'complement': {
                'type': 'string',
                'maxlength': 50
            },
            'city': {
                'type': 'string',
                'maxlength': 70
            }
        }
        super(AddressController, self).__init__(model, self.default_schema)


    def manipulate_get(self, entities):
        addresses_response = []
        for address in entities:
            address_dict = {
                'id': address.id,
                'cep': address.cep,
                'street': address.street,
                'number': address.number,
                'complement': address.complement,
                'city': address.city,
            }

            addresses_response.append(address_dict)

        return addresses_response
