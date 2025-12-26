# ROUTES FOR API #
from app.models import Contract, Partner
from app.extensions import db
from datetime import date
from sqlalchemy import select, Date
from flask import jsonify

from app.api_routes import api_bp

@api_bp.route('/api_contract_list/', methods = ['GET'])
def api_contract_list():
    stmt = select(Contract).limit(5)
    contracts = db.session.scalars(stmt).all()

    # building contract dicts for json
    contract_dicts = [
        {
            "contractID": c.contract_id,
            "registrationDate" : c.registration_date.strftime("%Y-%m-%d"),
            "contractTitle" : c.contract_title,
            "contractDescription" : c.contract_description,
            "contractNo": c.contract_no,
            "contractForm": "DPA" if c.contract_form else "DSA",
            "contractStatus" : c.contract_status,
            "partnerID" : "partnerID", #replace to a query to a partner's name
            "signed_date": c.signed_date.strftime("%Y-%m-%d"),
            "systemRegistered": "yes" if c.system_registered else "no",
            "reportedHQ": "yes" if c.HQ_reported else "no",
            "picID": c.PIC_id,
            "departmentID": c.PIC_team
        }
        for c in contracts
    ]

    # Wrap the dict structure
    response = { "contract_list": contract_dicts}


    return jsonify(response), 200