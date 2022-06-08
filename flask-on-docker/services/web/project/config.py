import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://GTN_Admin:GTNAdmin!123@localhost:5432/GTN_User")
    SQLALCHEMY_TRACK_MODIFICATIONS = False