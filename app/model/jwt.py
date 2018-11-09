from app import mongo

class Jwt(object):
    def __init__(self):
        self.collection = mongo.db.jwt


    def find_jwt(self, jti):
        jwt = self.collection.find_one({"jti": jti})
        return jwt


    def add_jwt(self, jti):
        result = self.collection.insert_one({'jti': jti})
        if result is not None:
            return True
        else:
            return False