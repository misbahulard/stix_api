import datetime
import json

from bson import ObjectId
from flask import request


class JSONEncoder(json.JSONEncoder):                           
    ''' extend json-encoder class'''
    
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)                               
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


def jsonify_stix(data):
    """ jsonify stix objects """
    result = json.dumps(data, cls=JSONEncoder)
    return json.loads(result)


def get_links(size, limit, offset):
    """ get self, prev, next url for pagination api response """

    next_offset = offset + limit
    prev_offset = (offset - limit) if (offset - limit) > 0 else 0
    self_url = request.base_url + "?limit=" + str(limit) + "&offset=" + str(offset)
    next_url = request.base_url + "?limit=" + str(limit) + "&offset=" + str(next_offset)
    prev_url = request.base_url + "?limit=" + str(limit) + "&offset=" + str(prev_offset)

    if prev_offset is 0:
        links = {
            "self": self_url,
            "next": next_url
        }
    elif next_offset >= size:
        links = {
            "self": self_url,
            "prev": prev_url
        }
    else:
        links = {
            "self": self_url,
            "next": next_url,
            "prev": prev_url
        }

    return links
