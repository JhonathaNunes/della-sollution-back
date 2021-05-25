from BaseController import BaseController

class UserController(BaseController):

    def __init__(self, model):
        self.post_schema = {
            'full_name': {
                'type': 'string',
                'maxlength': 200
            },
            'username': {
                'type': 'string',
                'maxlength': 65
            },
            'password': {
                'type': 'string',
                'maxlength': 20
            },
            'email': {
                'type': 'string',
                'maxlength': 65
            }
        }
        self.put_schema = {
            'full_name': {
                'type': 'string',
                'maxlength': 200
            },
            'username': {
                'type': 'string',
                'maxlength': 65
            },
            'email': {
                'type': 'string',
                'maxlength': 65
            }
        }
        super(UserController, self).__init__(model, self.post_schema, self.put_schema)


    def manipulate_get(self, entities):
        users_response = []
        for user in entities:
            user_dict = {
                'id': user.id,
                'full_name': user.full_name,
                'username': user.username,
                'email': user.email
            }
            users_response.append(user_dict)

        return users_response


    def manipulatePost(self, entity, request_data):
        entity.hash_password(request_data["password"])


    def manipulatePut(self, entity, request_data):
        if request_data["password"]:
            del request_data["password"]
            