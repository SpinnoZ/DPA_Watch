from datetime import datetime
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Partners(db.Model):
    __tablename__ = 'partners'
    partner_ID = db.Column(db.Integer, primary_key=True)
    partner_name = db.Column(db.String, nullable=False)
    tax_no = db.Column(db.Integer, unique=True, nullable=False)

    #relations
    contracts = relationship("Contracts", back_populates="partners")

class Contracts(db.Model):
    __tablename__ = 'contracts'
    contract_ID = db.Column(db.Integer, primary_key=True)
    registration_date = db.Column(db.Date, default=datetime.utcnow)
    contract_title = db.Column(db.String, nullable=False)
    contract_description = db.Column(db.String(120))
    contract_no = db.Column(db.String, nullable=False, unique=True)
    contract_status = db.Column(db.String, nullable=False)
    signed_date = db.Column(db.Date, nullable=True)
    system_registered = db.Column(db.Boolean, default=False)
    HQ_reported = db.Column(db.Boolean, default=False)
    contract_folder = db.Column(db.String, nullable=True)
    PIC_id = db.Column(db.String, nullable=False)
    PIC_team = db.Column(db.String, nullable=False)

    #relations
    partner_ID = db.Column(db.Integer, db.ForeignKey('partners.partner_ID'), nullable=False)
    partners = relationship("Partners", back_populates="contracts")
    audits = relationship("Audits", back_populates="contract")

class Audits(db.Model):
    __tablename__ = 'audits'
    audit_ID = db.Column(db.Integer, primary_key=True)
    audit_date = db.Column(db.Date, nullable=False)
    audit_type = db.Column(db.String, nullable=False)
    audit_status = db.Column(db.String, nullable=False)

    #relations
    contract_ID = db.Column(db.Integer, db.ForeignKey('contracts.contract_ID'), nullable=False)
    contract = relationship("Contracts", back_populates="audits")