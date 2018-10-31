from app import mongo
from app.utils import jsonify_stix


class AttackPattern(object):
    """ Attack Pattern model for access attack_pattern collection in mongodb """

    def __init__(self):
        self.collection = mongo.db.attack_pattern

    
    def get_all(self, limit, offset):
        attack_pattern_list = list(self.collection.find().skip(offset).limit(limit))
        result = jsonify_stix(attack_pattern_list)
        return result


    def find(self, id):
        result = jsonify_stix(self.collection.find_one({'id': id}))
        return result

    
    def count(self):
        result = self.collection.count()
        return result
