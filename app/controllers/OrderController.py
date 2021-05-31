import database
import exceptions
from flask import request, jsonify, g
from datetime import datetime
from authenticator import auth
from BaseController import BaseController
from cerberus import Validator
from sqlalchemy import exc
from models import (
    db,
    OrderStatus,
    Address,
    OrderServices,
    VisitStatus,
    Service,
    Material
)

class OrderController(BaseController):

    def __init__(self, model):
        self.default_schema = {
            'description': {
                'type': 'string',
                'maxlength': 255
            },
            'client_id': {
                'type': 'integer'
            },
            'address': {
                'type': 'dict'
            },
            'services': {
                'type': 'list'
            }
        }
        super(OrderController, self).__init__(model, self.default_schema)


    def manipulate_get(self, entities):
        orders_response = []
        for order in entities:
            order_services = []

            if (len(order.order_service) > 0):
                for order_service in order.order_service:
                    order_service_materials = []

                    if(len(order_service.service_material) > 0):
                        for order_service_material in order_service.service_material:
                            order_service_materials.append({
                                'id': order_service_material.id,
                                'material': {
                                    'id': order_service_material.material.id,
                                    'name': order_service_material.material.name,
                                    'description': order_service_material.material.description
                                },
                                'qtd': order_service_material.qtd,
                                'unique_value': order_service_material.unique_value
                            })

                    order_services.append({
                        'id': order_service.id,
                        'service': {
                            'id': order_service.service.id,
                            'name': order_service.service.name,
                            'description': order_service.service.description
                        },
                        'visit_status': {
                            'id': order_service.visit_status.id,
                            'status': order_service.visit_status.status,
                            'description': order_service.visit_status.description
                        },
                        'service_date': order_service.service_date,
                        'hours_worked': order_service.hours_worked,
                        'value_hour': order_service.value_hour,
                        'order_service_materials': order_service_materials
                    })

            order_dict = {
                'id': order.id,
                'client': {
                    'id': order.client.id,
                    'full_name': order.client.full_name,
                    'email': order.client.email,
                    'phone': order.client.phone,
                    'cnpj': order.client.cnpj,
                    'cpf': order.client.cpf
                },
                'user': {
                    'id': order.user.id,
                    'full_name': order.user.full_name,
                    'username': order.user.username,
                    'email': order.user.email
                },
                'address': {
                    'id': order.address.id,
                    'cep': order.address.cep,
                    'street': order.address.street,
                    'number': order.address.number,
                    'complement': order.address.complement,
                    'city': order.address.city
                },
                'order_status': {
                    'id': order.order_status.id,
                    'status': order.order_status.status,
                    'description': order.order_status.description
                },
                'description': order.description,
                'created_at': order.created_at,
                'updated_at': order.updated_at,
                'order_services': order_services
            }

            orders_response.append(order_dict)

        return orders_response


    @auth.login_required
    def post(self):
        request_data = request.get_json()
        v = Validator(require_all=True)

        if (not v.validate(request_data, self.post_schema)):
            return jsonify(v.errors), 422

        try:
            error = self.manipulate_post(request_data)
            if error is not None:
                return error

            datetime_value = datetime.now()
            user_id = g.user.id
            order_status = OrderStatus.query.filter_by(status='P').first()
            self.set_address(request_data)

            services = request_data['services']
            del request_data['services']

            request_data['user_id'] = user_id
            request_data['order_status_id'] = order_status.id
            request_data['created_at'] = datetime_value
            request_data['updated_at'] = datetime_value

            entity = self.model(**request_data)

            database.add_instance(entity)
            
            self.set_services(entity, services)

            return jsonify("success"), 200
        except exc.IntegrityError:
            return jsonify({"error": self.model + " already registred"}), 409

    
    def manipulate_put(self, entity, request_data):
        entity.updated_at = datetime.now()


    def set_address(self, request_data):
        address = request_data['address']
        props_address = ['cep', 'street', 'number']
        query_address = Address.query
        for prop in props_address:
            if prop in address: 
                query_address = query_address.filter(getattr(Address, prop)==address[prop])
        base_address = query_address.first()

        if (base_address is not None):
            request_data['address_id'] = base_address.id
        else:
            new_address = Address(**address)
            db.session.add(new_address)
            db.session.flush()
            db.session.commit()
            request_data['address_id'] = new_address.id
        
        del request_data['address']


    def set_services(self, entity, ids_services):
        visit_status = VisitStatus.query.filter_by(status='P').first()
        for id_service in ids_services:
            param_order_service = {}
            param_order_service['service_id'] = id_service
            param_order_service['order_id'] = entity.id
            param_order_service['visit_status_id'] = visit_status.id
            service = Service.query.filter_by(id=id_service).first()
            param_order_service['value_hour'] = service.value_hour
            new_order_service = OrderServices(**param_order_service)
            db.session.add(new_order_service)
        db.session.commit()


    @auth.login_required
    def finalizar(self, id: int):
        try:
            entity = self.model.query.get(id)
            payment = 0
            order_status = OrderStatus.query.filter_by(status='F').first()

            entity.order_status_id = order_status.id
            
            payment = 0
            for order_service in entity.order_service:
                payment += (order_service.hours_worked * order_service.value_hour)

                sum_material = 0
                for service_material in order_service.service_material:
                    material = Material.query.get(service_material.material_id)
                    material.storage -= service_material.qtd
                    sum_material += (service_material.qtd * service_material.unique_value)

                payment += sum_material
                
            entity.payment = payment
            database.update_instance(entity)

            return jsonify("success"), 200
        except exc.IntegrityError:
            return jsonify({"error": self.model + " already registred"}), 409
        except exceptions.NotFoundException:
            return jsonify({"error": self.model + " not found"}), 404


    def custom_routes(self, app, model_string):
        app.add_url_rule('/'+model_string+'/finalizar/<int:id>', model_string+'_finalizar', self.finalizar, methods=['PUT'])
        