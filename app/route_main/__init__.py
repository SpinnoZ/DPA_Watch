from flask import Blueprint

bp = Blueprint(
    'route_main', __name__,
    template_folder='templates', 
    static_folder='static')

from app.route_main import routes