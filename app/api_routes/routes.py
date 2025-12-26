# ROUTES FOR API #
from app.models import Contract, Partner
from app.extensions import db
from datetime import date
from sqlalchemy import select, Date
from flask import jsonify

from app.api_routes import api_bp

def contracts_to_dict(contracts):
       contract_dict = [
            {
                "contractID": c.contract_id,
                "registrationDate" : c.registration_date.isoformat() if isinstance(c.registration_date, date) else None,
                "contractTitle" : c.contract_title,
                "contractDescription" : c.contract_description,
                "contractNo": c.contract_no,
                "contractForm": "DPA" if c.contract_form else "DSA",
                "contractStatus" : c.contract_status,
                "partnerName" : c.partner.partner_name if c.partner else None, #replace to a query to a partner's name
                "signed_date": c.signed_date.isoformat() if c.signed_date else None,
                "systemRegistered": "yes" if c.system_registered else "no",
                "reportedHQ": "yes" if c.HQ_reported else "no",
                "picID": c.PIC_id,
                "departmentID": c.PIC_team
            }
            for c in contracts
        ]
       return {"contract_list":contract_dict}


@api_bp.route('/api_contract_list/', methods = ['GET'])
def api_contract_list():
    stmt = select(Contract).limit(5)
    contracts = db.session.scalars(stmt).all()

    # building contract dicts for json
    # contract_dicts = [
    #     {
    #         "contractID": c.contract_id,
    #         "registrationDate" : c.registration_date.isoformat() if isinstance(c.registration_date, date) else None,
    #         "contractTitle" : c.contract_title,
    #         "contractDescription" : c.contract_description,
    #         "contractNo": c.contract_no,
    #         "contractForm": "DPA" if c.contract_form else "DSA",
    #         "contractStatus" : c.contract_status,
    #         "partnerName" : c.partner.partner_name if c.partner else None, #replace to a query to a partner's name
    #         "signed_date": c.signed_date.isoformat() if c.signed_date else None,
    #         "systemRegistered": "yes" if c.system_registered else "no",
    #         "reportedHQ": "yes" if c.HQ_reported else "no",
    #         "picID": c.PIC_id,
    #         "departmentID": c.PIC_team
    #     }
    #     for c in contracts
    # ]
    contract_dicts = contracts_to_dict(contracts)

    # Wrap the dict structure
    # response = { "contract_list": contract_dicts}


    return jsonify(contract_dicts), 200

@api_bp.route('/api_contract/<int:contractID>', methods = ['GET'])
def api_contract(contractID):
    stmt = select(Contract).where(Contract.contract_id == contractID)
    contracts_query = db.session.scalar(stmt)
    return jsonify(contracts_to_dict([contracts_query])), 200