from flask import jsonify, g
from flask_cors import CORS
from GenerateRoute import GenerateRoute
from GenerateDefaultData import GenerateDefaultData
from authenticator import auth
from config import allowed_origin
from init import create_app
from models import User

app = create_app()
cors = CORS(app, resources={r"*": {"origins": allowed_origin}})

@app.route('/', methods=['GET'])
def check():
    return "Hello World"


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token, app)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/login', methods=['POST'])
@auth.login_required
def login():
    token = g.user.generate_auth_token(app)
    user = g.user.__dict__
    del user['_sa_instance_state']
    del user['password']
    return jsonify({
        'user': user,
        'token': token.decode('ascii')
    }), 200


GenerateRoute(app)
GenerateDefaultData()
app.run()
