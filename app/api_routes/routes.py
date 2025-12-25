# ROUTES FOR API #

from app.api_routes import api_bp

@api_bp.route('/contract_list/', methods = ['GET'])
def api_contract_list():
    return ('this is contract list api response'), 200