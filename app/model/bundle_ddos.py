from app import mongo
from app.utils import jsonify_stix

class Bundle(object):
    """ Bundle model for access bundle collection in mongodb """

    def __init__(self):
        self.collection = mongo.db.bundle_ddos

    
    def get_all(self, limit, offset, sort, filt):
        query = self.collection.find().skip(offset).limit(limit)
        query_size = self.collection.find()
        if filt is not None:
            query = self.collection.find({filt['id']: {'$regex': filt['value']}}).skip(offset).limit(limit)
            query_size = self.collection.find({filt['id']: {'$regex': filt['value']}})
        if sort is not None:
            query.sort(sort['id'], -1 if sort['desc'] else 1 )
        
        bundle_list = list(query)
        size = query_size.count()
        result = jsonify_stix(bundle_list)
        return result, size

    def find(self, id):
        result = jsonify_stix(self.collection.find_one({'id': id}))
        return result

    
    def count(self):
        result = self.collection.count()
        return result
