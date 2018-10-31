import json

from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from app import mongo
from app.model.threat_actor import ThreatActor
from app.utils import get_links

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('limit')
parser.add_argument('offset')

class AllThreatActor(Resource):
    @jwt_required
    def get(self):
        """ get all threat_actor using pagination default limit=20 """

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
        threat_actor = ThreatActor()
        threat_actor_data = threat_actor.get_all(limit, offset)
        size = threat_actor.count()

        # get links
        links = get_links(size, limit, offset)

        return {
            '_links': links,
            'limit': limit,
            'offset': offset,
            'data': threat_actor_data,
            'size': size
        }

class ThreatActorFind(Resource):
    @jwt_required
    def get(self, id):
        """ find stix object with specified id """

        threat_actor = ThreatActor()
        threat_actor_data = threat_actor.find(id)

        return threat_actor_data
