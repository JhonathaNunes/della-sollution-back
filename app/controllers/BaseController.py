import database
from flask import request, jsonify
from sqlalchemy import exc
from cerberus import Validator
from authenticator import auth
import exceptions

class BaseController(object):

    def __init__(self, model, post_schema = {}, put_schema = {}):
        self.model = model
        self.post_schema = post_schema
        if (len(put_schema) == 0): self.put_schema = post_schema
        else: self.put_schema = put_schema


    @auth.login_required
    def get(self):
        entities = database.get_all(self.model)
        dict_data = self.manipulate_get(entities)
        
        return jsonify(dict_data), 200


    def manipulate_get(self, entities):
        entities_response = []
        for entity in entities:
            entities_dict = {}
            entities_response.append(entities_dict)
        return entities_response


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

            entity = self.model(**request_data)

            database.add_instance(entity)

            return jsonify("success"), 200
        except exc.IntegrityError:
            return jsonify({"error": self.model + " already registred"}), 409


    def manipulate_post(self, request_data):
        pass


    @auth.login_required
    def put(self, id: int):
        request_data = request.get_json()
        v = Validator()

        if (not v.validate(request_data, self.put_schema)):
            return jsonify(v.errors), 422

        try:
            entity = self.model.query.get(id)

            self.manipulate_put(entity, request_data)

            database.update_instance(entity or self.model,
                                    **request_data)

            return jsonify("success"), 200
        except exc.IntegrityError:
            return jsonify({"error": self.model + " already registred"}), 409
        except exceptions.NotFoundException:
            return jsonify({"error": self.model + " not found"}), 404


    def manipulate_put(self, entity, request_data):
        pass 


    @auth.login_required
    def delete(self, id: int):
        try:
            entity = self.model.query.get(id)
            if (entity is not None):
                entity.active = False
                database.update_instance(entity)

            return jsonify("success"), 200
        except exceptions.NotFoundException:
            return jsonify({"error": self.model + " not found"}), 404

    
    def custom_routes(self, app, model_string):
        pass
