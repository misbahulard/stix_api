from app import mongo
from app.utils import jsonify_stix

class Event(object):
    """ Event model for access event collection in mongodb """

    def __init__(self):
        self.collection = mongo.db.event

    def alert_count(self):
        pipeline = [
                        {
                            "$group": {
                                "_id": "$alert_msg", 
                                "count": {"$sum": "$number_observed"}
                            }
                        },
                        {
                            "$sort": { "count": -1 }
                        } 
                    ]

        query = self.collection.aggregate(pipeline)
        event_list = list(query)
        event_list_limit = []
        if len(event_list) >= 10:
            for index in range(10):
                event_list_limit.append(event_list[index])
        else:
            for index in range(len(event_list)):
                event_list_limit.append(event_list[index])
        result = jsonify_stix(event_list_limit)
        return result
    
    def port_count(self):
        pipeline = [
                        {
                            "$group": {
                                "_id": "$dest_port", 
                                "count": {"$sum": "$number_observed"}
                            }
                        },
                        {
                            "$sort": { "count": -1 }
                        } 
                    ]

        query = self.collection.aggregate(pipeline)
        event_list = list(query)
        event_list_limit = []
        if len(event_list) >= 10:
            for index in range(10):
                event_list_limit.append(event_list[index])
        else:
            for index in range(len(event_list)):
                event_list_limit.append(event_list[index])
        result = jsonify_stix(event_list_limit)
        return result
