from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from cycling_app.config import Config


# A global SQLAlchemy object is created
db = SQLAlchemy()
# A global Flask-Marshmallow is created
ma = Marshmallow()


def create_app(config_object=Config):
    """Create and configure the Flask app"""
    app = Flask(__name__)
    # Config parameters are in config.py
    app.config.from_object(config_object)

    # Uses a helper function to initialise extensions
    initialize_extensions(app)

    # Routes from routes.py are included
    with app.app_context():
        # This line is required before marshmallow schemas to instantiate the models
        from cycling_app.models import Cycling
        # Include the routes from main_routes.py and api_routes.py
        from cycling_app.main_routes import main_bp
        from cycling_app.api_routes import api_bp
        # Create table in database if it was absent
        db.create_all()
        # print([column.name for column in Cycling.__table__.columns])
        
        app.register_blueprint(main_bp)
        app.register_blueprint(api_bp)
    return app

def initialize_extensions(app):
    """"Binds extensions and Flask application instance (app)"""
    # Flask-SQLAlchemy
    db.init_app(app)
    # Flask-Marshmallow
    ma.init_app(app)