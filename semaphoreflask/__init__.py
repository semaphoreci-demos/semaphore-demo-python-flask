from flask import Flask, flash
from flask_pymongo import PyMongo
import os

app = Flask('__name__', template_folder="./semaphoreflask/templates/")
app.config['SECRET_KEY'] = 'b6b462cf486aa21eee5719bf931a792e'
app.config["MONGO_URI"] = os.environ.get('DB') or os.environ.get('MONGODB_URI')

try:
    mongo = PyMongo(app)
except mongo.errors.ServerSelectionTimeoutError as err:
    flash(f'MongoDB server is not running', 'error')

from semaphoreflask import routes

app.register_error_handler(404, routes.page_not_found)
app.register_error_handler(500, routes.internal_server_error)
