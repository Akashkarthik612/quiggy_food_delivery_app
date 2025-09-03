import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'food_delivery.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    