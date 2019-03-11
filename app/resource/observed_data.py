import ast

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
parser.add_argument('sorted')
parser.add_argument('filtered')

class AllObservedData(Resource):
    @jwt_required
    def post(self):
        """ get all observed data using pagination default limit=5 """

        data = parser.parse_args()

        if data['limit'] is None:
            limit = 5
        else:
            limit = int(data['limit'])

        if data['offset'] is None:
            offset = 0
        else:
            offset = int(data['offset'])

        if data['sorted'] is not None:
            sort = ast.literal_eval(data['sorted'])
        else:
            sort = None

        if data['filtered'] is not None:
            filt = ast.literal_eval(data['filtered'])
        else:
            filt = None

        # get data
        observed_data = ObservedData()
        obs_data, size = observed_data.get_all(limit, offset, sort, filt)

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
