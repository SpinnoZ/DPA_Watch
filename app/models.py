from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import declarative_base, relationship, mapped_column
from datetime import date
from .extensions import db


class Contract(db.Model):
    __tablename__ = 'contracts'

    contract_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    registration_date = mapped_column(Date, default=date.today)
    contract_title = mapped_column(String(100), nullable=False)
    contract_description = mapped_column(String(120))
    contract_no = mapped_column(String(50), nullable=False)
    contract_form = mapped_column(Boolean, nullable=False)  # True for DPA, False for DSA
    contract_status = mapped_column(String(20), nullable=False)
    partner_id = mapped_column(ForeignKey('partners.partner_id'), nullable=True) # ATTENTION: CHANGE TO FALSE WHEN PARTNER DB LOGIC IS READY!
    signed_date = mapped_column(Date)
    system_registered = mapped_column(Boolean, default=False)
    HQ_reported = mapped_column(Boolean, default=False)
    contract_folder = mapped_column(String(200))
    PIC_id = mapped_column(String(100))
    PIC_team = mapped_column(String(100))
    
    # Relationship to "Partner" table
    partner = relationship("Partner", back_populates="contracts")
    
    # Relationship to "Audits" table
    audits = relationship("Audit", back_populates="contract")

class Partner(db.Model):
    __tablename__ = 'partners'

    partner_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    partner_name = mapped_column(String(100), nullable=False)
    tax_no = mapped_column(Integer, nullable=False)

    # Relationship to "Contract" table
    contracts = relationship("Contract", back_populates="partner")

class Audit(db.Model):
    __tablename__ = 'audits'

    audit_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    audit_date = mapped_column(Date, nullable=False)
    audit_type = mapped_column(String(20), nullable=False)  # Options: "documentary" or "onsite"
    audit_status = mapped_column(String(20), nullable=False)  # Options: "planned", "done_clear", "done_findings", "done_fixed"
    contract_id = mapped_column(ForeignKey('contracts.contract_id'), nullable=False)

    # Relationship to "Contract" table
    contract = relationship("Contract", back_populates="audits")