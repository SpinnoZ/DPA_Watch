from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, DateField, FileField, TextAreaField, RadioField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, InputRequired

class ContractForm(FlaskForm):
    contract_title = StringField('Contract Title', validators=[DataRequired()])
    contract_description = TextAreaField('Description', validators=[Length(max=120)])
    contract_no = StringField('Contract RUS Number', validators=[DataRequired()])
    contract_form = SelectField('DPA/DSA', choices=[(True, 'DPA'), (False, 'DSA')], coerce=bool)
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
    files = FileField('Attach Files (Max 10MB per file)', render_kw={"multiple": True})
    submit = SubmitField('Submit')

class PartnerForm(FlaskForm):
    partner_name = StringField('Name', validators=[DataRequired()])
    tax_no = IntegerField('Tax No', validators=[DataRequired()]) # ADD Validation for INN