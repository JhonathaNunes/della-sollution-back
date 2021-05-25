from sys import path
path.append('./app/controllers')
from flask import Flask
from models import (
    Client,
    Service,
    Material,
    User,
    Orders,
    Address,
    EvaluationVisits,
    OrderServices,
    ServiceMaterials
)
from MaterialController import MaterialController
from UserController import UserController
from ClientController import ClientController
from ServiceController import ServiceController
from OrderController import OrderController
from AddressController import AddressController
from EvaluationVisitController import EvaluationVisitController
from OrderServiceController import OrderServiceController
from ServiceMaterialController import ServiceMaterialController

class GenerateRoute():

    def __init__(self, app: Flask):
        self.app = app
        self.controllers = {
            UserController: User,
            ClientController: Client,
            ServiceController: Service,
            MaterialController: Material,
            OrderController: Orders,
            AddressController: Address,
            EvaluationVisitController: EvaluationVisits,
            OrderServiceController: OrderServices,
            ServiceMaterialController: ServiceMaterials
        }
        self.generate_routes()


    def generate_routes(self):
        for key, value in self.controllers.items():
            model_string = value.__name__.lower()
            controller = key(value)
            self.default_routes(controller, model_string)
            self.custom_routes(controller, model_string)
            

    def default_routes(self, controller, model_string):
        self.app.add_url_rule('/'+model_string, model_string+'_get', controller.get, methods=['GET'])
        self.app.add_url_rule('/'+model_string, model_string+'_post', controller.post, methods=['POST'])
        self.app.add_url_rule('/'+model_string+'/<int:id>', model_string+'_put', controller.put, methods=['PUT'])
        self.app.add_url_rule('/'+model_string+'/<int:id>', model_string+'_delete', controller.delete, methods=['DELETE'])


    def custom_routes(self, controller, model_string):
        controller.custom_routes(self.app, model_string)
        