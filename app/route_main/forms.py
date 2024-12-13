from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, DateField, TextAreaField, RadioField, SubmitField, IntegerField, MultipleFileField
from wtforms.validators import DataRequired, Length, Optional, InputRequired, ValidationError
from app.models import Partner

class ContractForm(FlaskForm):

    def coerce_bool(x):
        if isinstance(x, str):
            return x == "True" if x != "None" else None
        else:
            return bool(x) if x is not None else None

    contract_title = StringField('Contract Title', validators=[DataRequired()])
    contract_description = TextAreaField('Description', validators=[Length(max=120)])
    contract_no = StringField('Contract RUS Number', validators=[DataRequired()])
    contract_form = SelectField('DPA/DSA', validators=[InputRequired()], 
                                choices=[(True, 'DPA'), (False, 'DSA')], 
                                coerce=coerce_bool)
    ## lambda x: x == 'True'
    contract_status = SelectField('Status', validators=[Optional()], choices=[
        ('drafted', 'Drafted'),
        ('confirmed', 'Confirmed'),
        ('signed', 'Signed'),
        ('terminated', 'Terminated')
    ])
    signed_date = DateField('Signed Date', format='%Y-%m-%d', validators=[Optional()])
    system_registered = BooleanField('System Registered')
    HQ_reported = BooleanField('HQ Reported')
    PIC_id = StringField('Person in Charge ID', validators=[DataRequired()])
    PIC_team = StringField('Person in Charge Team', validators=[DataRequired()])
    files = MultipleFileField('Attach Files (Max 10MB per file)', render_kw={"multiple": True})
    partner_name = StringField('Name', validators=[DataRequired()])
    tax_no = IntegerField('Tax No', validators=[DataRequired()]) # ADD Validation for INN
    submit = SubmitField('Submit')

    def validate(self, extra_validators=None):
        # Call the parent validate method
        initial_validation = super(ContractForm, self).validate(extra_validators)
        # 
        if not initial_validation:
            return False

        # Get the data from the form
        partner_name = self.partner_name.data
        tax_no = self.tax_no.data

        # Check if the partner_name exists in the database
        existing_partner = Partner.query.filter_by(partner_name=partner_name).first()
        print(f'Partner name: {partner_name}')
        print(existing_partner)
        print('================')
        if existing_partner:
            if existing_partner.tax_no != tax_no:
                print('partner name error')
                self.partner_name.errors.append("This partner name has another tax number.")
                return False

        # Check if the tax_no exists in the database
        existing_partner_by_tax_no = Partner.query.filter_by(tax_no=tax_no).first()
        if existing_partner_by_tax_no:
            if existing_partner_by_tax_no.partner_name != partner_name:
                print('repeated tax number error')
                self.tax_no.errors.append("This tax number is assigned to another partner.")
                return False

        return True

class NewPartnerForm(FlaskForm):
    partner_name = StringField('Name', validators=[DataRequired()])
    tax_no = IntegerField('Tax No', validators=[DataRequired()]) # ADD Validation for INN
    submit = SubmitField('Submit')