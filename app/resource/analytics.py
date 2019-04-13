import ast

from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app import mongo
from app.model.event import Event
from app.model.actor_analytics import ActorAnalytics
from app.model.target_analytics import TargetAnalytics
from app.utils import get_links

class AlertCount(Resource):
    @jwt_required
    def get(self):
        """ get alert count """

        # get data
        event = Event()
        event_data = event.alert_count()

        return event_data

class PortCount(Resource):
    @jwt_required
    def get(self):
        """ get port count """

        # get data
        event = Event()
        event_data = event.port_count()

        return event_data

class ActorCount(Resource):
    @jwt_required
    def get(self):
        """ get actor count """

        # get data
        event = ActorAnalytics()
        event_data = event.get_actor_count()

        return event_data

class ActorCountryCount(Resource):
    @jwt_required
    def get(self):
        """ get actor country count """

        # get data
        event = ActorAnalytics()
        event_data = event.get_actor_country_count()

        return event_data
        
class TargetCount(Resource):
    @jwt_required
    def get(self):
        """ get target count """

        # get data
        event = TargetAnalytics()
        event_data = event.get_target_count()

        return event_data

class TargetCountryCount(Resource):
    @jwt_required
    def get(self):
        """ get target country count """

        # get data
        event = TargetAnalytics()
        event_data = event.get_target_country_count()

        return event_data
