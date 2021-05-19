from flask import request, jsonify
from BaseController import BaseController
from models import (
    Material
)
import exceptions

class ServiceMaterialController(BaseController):

    def __init__(self, model):
        self.default_schema = {
            'material_id': {
                'type': 'integer'
            },
            'order_service_id': {
                'type': 'integer'
            },
            'qtd': {
                'type': 'integer'
            },
            'unique_value': {
                'type': 'float'
            }
        }
        super(ServiceMaterialController, self).__init__(model, self.default_schema)


    def manipulate_get(self, entities):
        service_material_response = []
        for service_material in entities:

            service_material_dict = {
                'id': service_material.id,
                'material_id': service_material.material_id,
                'material': {
                    'id': service_material.material.id,
                    'name': service_material.material.name,
                    'description': service_material.material.description,
                    'storage': service_material.material.storage,
                    'unique_value': "{:.3f}".format(service_material.material.unique_value).rstrip('0')
                },
                'order_service': {
                    'id': service_material.order_service.id,
                    'service_id': service_material.order_service.service_id,
                    'order_id': service_material.order_service.order_id,
                    'visit_status_id': service_material.order_service.visit_status_id,
                    'service_date': service_material.order_service.service_date,
                    'hours_worked': service_material.order_service.hours_worked,
                    'value_hour': service_material.order_service.value_hour
                },
                'qtd': service_material.qtd,
                'unique_value': service_material.unique_value
            }
            service_material_response.append(service_material_dict)

        return service_material_response

    
    def manipulate_post(self, request_data):
        #Verifica se tem materiais suficientes no estoque para a ordem do serviço
        return self.ajusta_storage(request_data)
        
    
    def ajusta_storage(self, request_data):
        try:
            material_id = request_data['material_id']
            qtde = request_data['qtd']
            material = Material.query.get(material_id)
            if (qtde > material.storage):
                return jsonify({"error": "Não existe a quantidade de materiais no estoque para a ordem do serviço"}), 409
            else:
                material.storage -= qtde
                return None
        except exceptions.NotFoundException:
            return jsonify({"error": "Material not found"}), 404
        