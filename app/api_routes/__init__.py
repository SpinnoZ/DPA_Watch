from flask import Blueprint


api_bp = Blueprint(
    'api_routes', __name__,
    url_prefix='/api',
    template_folder='templates', 
    static_folder='static')

from app.api_routes import routes