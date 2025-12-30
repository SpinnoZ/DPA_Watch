from flask import Flask
from flask_wtf import CSRFProtect
from config import Config
from .extensions import db
from flask_cors import CORS


#csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, origins=["http://localhost:5173"])

    # # # INITIALIZE EXTENSIONS # # #
    from . import models
    db.init_app(app)
    #csrf.init_app(app)
   
    # # # REGISTER BLUEPRINTS # # #
    from app.route_main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.api_routes import api_bp as api_bp
    app.register_blueprint(api_bp)

    # with app.app_context():
    #     from . import routes
    #     db.create_all()
    return app