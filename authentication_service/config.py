class Config(object):
    # config database
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:auth@192.168.1.105:3306/authentication'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_TIMEOUT = 28800
    SQLALCHEMY_POOL_RECYCLE = 1000

    # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_CONNECTION_STRING')
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_POOL_TIMEOUT'] = 800
    # app.config['SQLALCHEMY_POOL_RECYCLE'] = 100

class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:auth@192.168.1.13:3306/authentication'