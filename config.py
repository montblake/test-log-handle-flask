import os
from dotenv import load_dotenv

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    IMDB_KEY = os.environ.get('IMDB_KEY')
    OMDB_KEY = os.environ.get('OMDB_KEY')
    