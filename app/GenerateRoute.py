from flask import Flask
from models import (
    Client,
    Service,
    Material,
    User,
    Orders,
    Address,
    EvaluationVisits
)
from MaterialController import MaterialController
from UserController import UserController
from ClientController import ClientController
from ServiceController import ServiceController
from OrderController import OrderController
from AddressController import AddressController
from EvaluationVisitController import EvaluationVisitController

class GenerateRoute(object):

    def __init__(self, app: Flask):
        self.app = app
        self.controllers = {
            UserController: User,
            ClientController: Client,
            ServiceController: Service,
            MaterialController: Material,
            OrderController: Orders,
            AddressController: Address,
            EvaluationVisitController: EvaluationVisits
        }
        self.generateRoutes()


    def generateRoutes(self):
        for key, value in self.controllers.items():
            modelString = value.__name__.lower()
            controller = key(value, self.app)
            self.app.add_url_rule('/'+modelString, modelString+'Get', controller.get, methods=['GET'])
            self.app.add_url_rule('/'+modelString, modelString+'Post', controller.post, methods=['POST'])
            self.app.add_url_rule('/'+modelString+'/<int:id>', modelString+'Put', controller.put, methods=['PUT'])
            self.app.add_url_rule('/'+modelString+'/<int:id>', modelString+'Delete', controller.delete, methods=['DELETE'])
        