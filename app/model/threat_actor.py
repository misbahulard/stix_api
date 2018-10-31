from app import mongo
from app.utils import jsonify_stix


class ThreatActor(object):
    """ Threat Actor model for access threat_actor collection in mongodb """

    def __init__(self):
        self.collection = mongo.db.threat_actor

    
    def get_all(self, limit, offset):
        threat_actor_list = list(self.collection.find().skip(offset).limit(limit))
        result = jsonify_stix(threat_actor_list)
        return result


    def find(self, id):
        result = jsonify_stix(self.collection.find_one({'id': id}))
        return result

    
    def count(self):
        result = self.collection.count()
        return result