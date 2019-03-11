class Config():
    SECRET_KEY = 'akuwumbodiawumbokitawumbo'
    MONGO_URI = 'mongodb://localhost:27017/stix_test'
    JWT_SECRET_KEY = 'my-jwt-secret-key'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']