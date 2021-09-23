from flask import Flask
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os
from flask import has_request_context, request
from flask.logging import default_handler
from flask_paranoid import Paranoid

app = Flask(__name__)
app.config.from_object(Config)

paranoid = Paranoid(app)
paranoid.redirect_view = '/'

class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)

formatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
)



# if there is not a logs directory, make one
if not os.path.exists('logs'):
    os.mkdir('logs')
# set up a file handler object
file_handler = RotatingFileHandler('logs/test-log-handle.log', maxBytes=10240, backupCount=10)
#  write to file under these circumstances
# low to high: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.DEBUG)
app.logger.info('TestLogHandleApp startup')


from app import routes, errors