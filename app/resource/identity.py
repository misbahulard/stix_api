import json

from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from app import mongo
from app.model.identity import Identity
from app.utils import get_links

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('limit')
parser.add_argument('offset')

class AllIdentity(Resource):
    @jwt_required
    def get(self):
        """ get all identity using pagination default limit=20 """

        data = parser.parse_args()

        if data['limit'] is None:
            limit = 20
        else:
            limit = int(data['limit'])

        if data['offset'] is None:
            offset = 0
        else:
            offset = int(data['offset'])

        # get data
        identity = Identity()
        identity_data = identity.get_all(limit, offset)
        size = identity.count()

        # get links
        links = get_links(size, limit, offset)

        return {
            '_links': links,
            'limit': limit,
            'offset': offset,
            'data': identity_data,
            'size': size
        }

class IdentityFind(Resource):
    @jwt_required
    def get(self, id):
        """ find stix object with specified id """

        identity = Identity()
        identity_data = identity.find(id)

        return identity_data
