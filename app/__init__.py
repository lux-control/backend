import os
from flask import Flask
from app.extensions import mongo

from .main.routes import main_bp
from .auth.routes import auth_bp
from .device.routes import device_bp

from dotenv import load_dotenv, find_dotenv

def create_app():

    load_dotenv(find_dotenv())
    
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    mongo.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(device_bp)
    return app