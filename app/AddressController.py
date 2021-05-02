
from flask import Flask
from BaseController import BaseController

class AddressController(BaseController):

    def __init__(self, model, app: Flask):
        self.schema = {}
        super(AddressController, self).__init__(model, app, self.schema)


    def manipulateGet(self, entities):
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
