from app import mongo
from passlib.hash import pbkdf2_sha256 as sha256

class User(object):
    def __init__(self):
        self.collection = mongo.db.user


    def find_user(self, username):
        user = self.collection.find_one({"username": username})
        return user


    def add_user(self, obj):
        result = self.collection.insert_one(obj)
        if result is not None:
            return True
        else:
            return False

    
    def delete_user(self, username):
        result = self.collection.delete_one({'username': username}).deleted_count
        if result == 1:
            return True
        else:
            return False


    def get_all_user(self):
        user_list = list(self.collection.find())
        users = map(lambda x: self.to_json(x), user_list)
        return users
        

    def to_json(self, x):
        return {
            'username': x['username'],
            'password': x['password']
        }

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
