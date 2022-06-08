import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://{DB['GTN_Admin']}:{DB['GTNAdmin!123']}@{DB['db:5432']}/{DB['GTN_User']}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False