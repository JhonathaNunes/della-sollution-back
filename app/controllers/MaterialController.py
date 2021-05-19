from BaseController import BaseController

class MaterialController(BaseController):

    def __init__(self, model):
        self.default_schema = {
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
        super(MaterialController, self).__init__(model, self.default_schema)


    def manipulate_get(self, entities):
        materials_response = []
        for material in entities:
            materials_dict = {
                'id': material.id,
                'name': material.name,
                'description': material.description,
                'storage': material.storage,
                'unique_value': "{:.3f}".format(material.unique_value).rstrip('0')
            }
            materials_response.append(materials_dict)
        return materials_response
