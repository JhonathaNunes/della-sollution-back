from BaseController import BaseController
from flask import request, jsonify
from BaseController import BaseController
from models import (
    db,
    Material,
    ServiceMaterials
)

class OrderServiceController(BaseController):

    def __init__(self, model):
        self.default_schema = {
            'service_id': {
                'type': 'integer'
            },
            'order_id': {
                'type': 'integer'
            },
            'visit_status_id': {
                'type': 'integer'
            },
            'service_date': {
                'type': 'datetime'
            },
            'hours_worked': {
                'type': 'float'
            },
            'value_hour': {
                'type': 'float'
            },
            'new_materials': {
                'type': 'list',
                'required': False
            }
        }
        super(OrderServiceController, self).__init__(model, self.default_schema)


    def manipulate_get(self, entities):
        order_service_response = []
        for order_service in entities:

            order_service_dict = {
                'id': order_service.id,
                'service': {
                    'id': order_service.service.id,
                    'name': order_service.service.name,
                    'description': order_service.service.description,
                    'value_hour': "{:.2f}".format(order_service.service.value_hour).rstrip('0')
                },
                'order' : {
                    'id': order_service.order.id,
                    'client_id': order_service.order.client_id,
                    'user_id': order_service.order.user_id,
                    'address_id': order_service.order.address_id,
                    'order_status_id': order_service.order.order_status_id,
                    'description': order_service.order.description,
                    'created_at': order_service.order.created_at,
                    'updated_at': order_service.order.updated_at
                },
                'visit_status' : {
                    'id': order_service.visit_status.id,
                    'status': order_service.visit_status.status,
                    'description': order_service.visit_status.description
                },
                'service_date': order_service.service_date,
                'hours_worked': order_service.hours_worked,
                'value_hour': order_service.value_hour
            }
            order_service_response.append(order_service_dict)

        return order_service_response


    def manipulate_put(self, entity, request_data):
        if request_data["new_materials"]:
            new_materials = request_data["new_materials"]
            for new_material in new_materials:
                param_service_material = {}
                material = Material.query.filter_by(id=new_material['id']).first()

                param_service_material['order_service_id'] = entity.id
                param_service_material['material_id'] = material.id
                param_service_material['unique_value'] = material.unique_value
                param_service_material['qtd'] = new_material['qtd']
                new_service_material = ServiceMaterials(**param_service_material)
                db.session.add(new_service_material)
            db.session.commit()
