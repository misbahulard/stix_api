from app import mongo
from app.utils import jsonify_stix


class Indicator(object):
    """ Indicator model for access indicator collection in mongodb """

    def __init__(self):
        self.collection = mongo.db.indicator

    
    def get_all(self, limit, offset, sort, filt):
        query = self.collection.find().skip(offset).limit(limit)
        if filt is not None:
            query = self.collection.find({filt['id']: {'$regex': filt['value']}}).skip(offset).limit(limit)
        if sort is not None:
            query.sort(sort['id'], -1 if sort['desc'] else 1 )

        indicator_list = list(query)
        result = jsonify_stix(indicator_list)
        return result


    def find(self, id):
        result = jsonify_stix(self.collection.find_one({'id': id}))
        return result

    
    def count(self):
        result = self.collection.count()
        return result
