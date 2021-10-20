from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
from config import config
from flask_assets import Environment, Bundle
from .util.assets import bundles
from elasticsearch import Elasticsearch

db = SQLAlchemy()
assets = Environment()
# login_manager = LoginManager()
# login_manager.login_view =  "auth.login"

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app) 

    db.init_app(app)
    assets.init_app(app)
    #login_manager.init_app(app)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    # if app.config["SSL_REDIRECT"]:
    #         from flask_sslify import SSLify
    #         sslify = SSLify(app)

    assets.register(bundles)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app