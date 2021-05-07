import database
from flask import Flask, request, jsonify
from sqlalchemy import exc
from cerberus import Validator
import exceptions

class BaseController(object):

    def __init__(self, model, app: Flask, schema):
        self.model = model
        self.app = app
        self.schema = schema

    
    def get(self):
        entities = database.get_all(self.model)
        dictData = self.manipulateGet(entities)
        
        return jsonify(dictData), 200


    def manipulateGet(self, entities):
        entities_response = []
        for entity in entities:
            entities_dict = {}
            entities_response.append(entities_dict)
        return entities_response


    def post(self):
        request_data = request.get_json()
        v = Validator(require_all=True)

        if (not v.validate(request_data, self.schema)):
            return jsonify(v.errors), 422

        try:
            entity = self.model(**request_data)

            self.manipulatePost(entity, request_data)

            database.add_instance(entity)

            return jsonify("success"), 200
        except exc.IntegrityError:
            return jsonify({"error": self.model + " already registred"}), 409

    def manipulatePost(self, entity, request_data):
        pass 


    def put(self, id: int):
        request_data = request.get_json()
        v = Validator()

        if (not v.validate(request_data, self.schema)):
            return jsonify(v.errors), 422

        try:
            entity = self.model.query.get(id)

            self.manipulatePut(entity, request_data)

            database.update_instance(entity or self.model,
                                    **request_data)

            return jsonify("success"), 200
        except exc.IntegrityError:
            return jsonify({"error": self.model + " already registred"}), 409
        except exceptions.NotFoundException:
            return jsonify({"error": self.model + " not found"}), 404


    def manipulatePut(self, entity, request_data):
        pass 

    
    def delete(self, id: int):
        try:
            database.delete_instance(self.model, id)

            return jsonify("success"), 200
        except exceptions.NotFoundException:
            return jsonify({"error": self.model + " not found"}), 404
