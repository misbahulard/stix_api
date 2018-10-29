from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_restful import Api
from werkzeug.security import safe_str_cmp

from utils import JSONEncoder
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.json_encoder = JSONEncoder

jwt = JWTManager(app)
mongo = PyMongo(app)
api = Api(app)

# blacklist loader to check if token already blacklist
from model.jwt import Jwt

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    jwt = Jwt()

    if jwt.find_jwt(jti) is not None:
        return True
    else:
        return False

from resource import user

api.add_resource(user.UserRegistration, '/registration')
api.add_resource(user.UserLogin, '/login')
api.add_resource(user.UserDelete, '/user/delete')
api.add_resource(user.UserLogoutAccess, '/logout/access')
api.add_resource(user.UserLogoutRefresh, '/logout/refresh')
api.add_resource(user.TokenRefresh, '/token/refresh')
api.add_resource(user.AllUsers, '/users')
api.add_resource(user.SecretResource, '/secret')
