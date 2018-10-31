import json

from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from app import mongo
from app.model.attack_pattern import AttackPattern
from app.utils import get_links

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('limit')
parser.add_argument('offset')

class AllAttackPattern(Resource):
    @jwt_required
    def get(self):
        """ get all attack_pattern using pagination default limit=20 """

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
        attack_pattern = AttackPattern()
        attack_pattern_data = attack_pattern.get_all(limit, offset)
        size = attack_pattern.count()

        # get links
        links = get_links(size, limit, offset)

        return {
            '_links': links,
            'limit': limit,
            'offset': offset,
            'data': attack_pattern_data,
            'size': size
        }

class AttackPatternFind(Resource):
    @jwt_required
    def get(self, id):
        """ find stix object with specified id """

        attack_pattern = AttackPattern()
        attack_pattern_data = attack_pattern.find(id)

        return attack_pattern_data
