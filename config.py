class Configuration:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cats_blog.db'
    SECRET_KEY = 'c002f87c097800ff73ecc497555f0c488695a69b'
    MAX_CONTENT_LENGTH = 1920 * 1920
    UPLOAD_FOLDER = 'static/img'
