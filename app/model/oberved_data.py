from app import mongo
from app.utils import jsonify_stix


class ObservedData(object):
    """ Observed Data model for access observed_data collection in mongodb """

    def __init__(self):
        self.collection = mongo.db.observed_data

    
    def get_all(self, limit, offset):
        observed_data_list = list(self.collection.find().skip(offset).limit(limit))
        result = jsonify_stix(observed_data_list)
        return result


    def find(self, id):
        result = jsonify_stix(self.collection.find_one({'id': id}))
        return result

    
    def count(self):
        result = self.collection.count()
        return result
