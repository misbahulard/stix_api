from app import mongo
from app.utils import jsonify_stix
from bson.son import SON
from bson.regex import Regex


class ObservedData(object):
    """ Observed Data model for access observed_data collection in mongodb """

    def __init__(self):
        self.collection = mongo.db.observed_data

    
    def get_all(self, limit, offset, sort, filt):
        query = self.collection.find().skip(offset).limit(limit)
        query_size = self.collection.find()

        if filt is not None:
            if filt['id'] != "objects.2.dst_port":
                query = self.collection.find({filt['id']: {'$regex': filt['value']}}).skip(offset).limit(limit)
            else:
                # Jika filter berdasarkan destination port => INTEGER!
                # maka harus pake cara BEGO (REGEX)
                regx = Regex("^"+filt['value']+".*")
                # jika dia disorting maka lakukan sort via aggregate
                if sort is not None:
                    pipeline = [
                        { "$addFields": { 
                            "stringifyExample": { "$toLower": "$objects.2.dst_port" }
                        }}, 
                        { "$match": { "stringifyExample": regx } },
                        {"$sort": SON([(sort['id'], -1 if sort['desc'] else 1)])}
                    ]
                else:
                    pipeline = [
                        { "$addFields": { 
                            "stringifyExample": { "$toLower": "$objects.2.dst_port" }
                        }}, 
                        { "$match": { "stringifyExample": regx } },
                    ]
                query = self.collection.aggregate(pipeline)

            query_size = self.collection.find({filt['id']: {'$regex': filt['value']}})

        if sort is not None:
            # Jika ada filter dan dia cari destination port, SKIP
            # selain itu sorting!
            if filt is not None and filt['id'] == "objects.2.dst_port":                
                pass
            else:
                query.sort(sort['id'], -1 if sort['desc'] else 1 )
        observed_data_list = list(query)
        size = query_size.count()
        result = jsonify_stix(observed_data_list)
        return result, size


    def find(self, id):
        result = jsonify_stix(self.collection.find_one({'id': id}))
        return result

    
    def count(self):
        result = self.collection.count()
        return result
