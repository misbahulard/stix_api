from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_restful import Api

from utils import JSONEncoder
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.json_encoder = JSONEncoder

CORS(app)
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

from resource import user, observed_data, indicator, identity, threat_actor, attack_pattern, bundle, analytics

# user
api.add_resource(user.UserRegistration, '/api/v1/registration')
api.add_resource(user.UserLogin, '/api/v1/login')
api.add_resource(user.UserDelete, '/api/v1/user/delete')
api.add_resource(user.UserLogoutAccess, '/api/v1/logout/access')
api.add_resource(user.UserLogoutRefresh, '/api/v1/logout/refresh')
api.add_resource(user.TokenRefresh, '/api/v1/token/refresh')
api.add_resource(user.AllUsers, '/api/v1/users')

# observed-data
api.add_resource(observed_data.AllObservedData, '/api/v1/observed-datas')
api.add_resource(observed_data.ObservedDataFind, '/api/v1/observed-datas/<string:id>')

# indicator
api.add_resource(indicator.AllIndicator, '/api/v1/indicators')
api.add_resource(indicator.IndicatorFind, '/api/v1/indicators/<string:id>')

# identity
api.add_resource(identity.AllIdentity, '/api/v1/identities')
api.add_resource(identity.IdentityFind, '/api/v1/identities/<string:id>')

# threat actor
api.add_resource(threat_actor.AllThreatActor, '/api/v1/threat-actors')
api.add_resource(threat_actor.ThreatActorFind, '/api/v1/threat-actors/<string:id>')

# attack pattern
api.add_resource(attack_pattern.AllAttackPattern, '/api/v1/attack-patterns')
api.add_resource(attack_pattern.AttackPatternFind, '/api/v1/attack-patterns/<string:id>')

# bundle
api.add_resource(bundle.AllBundle, '/api/v1/bundles')
api.add_resource(bundle.BundleFind, '/api/v1/bundles/<string:id>')

# analytics
api.add_resource(analytics.AlertCount, '/api/v1/analytics/alert-count')
api.add_resource(analytics.PortCount, '/api/v1/analytics/port-count')
api.add_resource(analytics.ActorCount, '/api/v1/analytics/actor-count')
api.add_resource(analytics.TargetCount, '/api/v1/analytics/target-count')
api.add_resource(analytics.ActorCountryCount, '/api/v1/analytics/actor-country-count')
api.add_resource(analytics.TargetCountryCount, '/api/v1/analytics/target-country-count')
