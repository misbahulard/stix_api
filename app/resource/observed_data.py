import json

from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from app import mongo
from app.model.oberved_data import ObservedData
from app.utils import get_links

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('limit')
parser.add_argument('offset')

class AllObservedData(Resource):
    @jwt_required
    def get(self):
        """ get all observed data using pagination default limit=20 """

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
        observed_data = ObservedData()
        obs_data = observed_data.get_all(limit, offset)
        size = observed_data.count()

        # get links
        links = get_links(size, limit, offset)

        return {
            '_links': links,
            'limit': limit,
            'offset': offset,
            'data': obs_data,
            'size': size
        }

class ObservedDataFind(Resource):
    @jwt_required
    def get(self, id):
        """ find stix object with specified id """

        observed_data = ObservedData()
        obs_data = observed_data.find(id)

        return obs_data
