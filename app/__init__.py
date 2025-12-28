import os
from flask import Flask
from app.extensions import mongo

from dotenv import load_dotenv, find_dotenv

def create_app():

    load_dotenv(find_dotenv())
    
    app = Flask(__name__)

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    mongo.init_app(app)
    return app