import json

from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, get_raw_jwt,
                                jwt_refresh_token_required, jwt_required)
from flask_restful import Resource, reqparse

from app import mongo
from app.model.user import User

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        username = data['username']
        password = User.generate_hash(data['password'])

        user = User()
        user_data = user.find_user(username)

        try:
            if user_data is None:
                # mongo.db.user.insert_one({'username': username, 'password': password})
                user.add_user({'username': username, 'password': password})
                access_token = create_access_token(identity=username)
                refresh_token = create_refresh_token(identity=username)
                return {
                    'message': 'User {} was created'.format(username),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                    }
            else:
                return {'message': 'User already exist'}
        except:
             return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        username = data['username']
        password = data['password']

        user = User()
        user_data = user.find_user(username)

        if user_data is None:
            return {'message': 'User {} doesn\'t exist'.format(username)}
        current_password = user_data['password']
        if User.verify_hash(password, current_password):
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return {
                'message': 'Login Success',
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': 'Login Failed'}
      

class UserDelete(Resource):
    def delete(self):
        data = parser.parse_args()
        username = data['username']
        user = User()

        if user.delete_user(username):
            return {'message': 'Delete success'}
        else:
            return {'message': 'Failed to delete user'}
      
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            mongo.db.jwt.insert_one({'jti', jti})
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
      
      
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            mongo.db.jwt.insert_one({'jti', jti})
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
      
      
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}
      

class AllUsers(Resource):
    def get(self):
        user = User()
        return {'users': user.get_all_user()}
      
      
class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }
