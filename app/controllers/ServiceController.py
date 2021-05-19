from BaseController import BaseController

class ServiceController(BaseController):

    def __init__(self, model):
        self.default_schema = {
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
        super(ServiceController, self).__init__(model, self.default_schema)


    def manipulate_get(self, entities):
        services_response = []
        for service in entities:
            service_dict = {
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'value_hour': "{:.2f}".format(service.value_hour).rstrip('0')
            }
            services_response.append(service_dict)

        return services_response
        