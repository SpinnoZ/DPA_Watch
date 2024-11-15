import os
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models import Contract, Partner, Audit
from .forms import ContractForm, PartnerForm
from app.route_main import bp

# New contract route
@bp.route('/new_contract/', methods=['GET', 'POST'])
def new_contract():
    form = ContractForm()
    partner_form = PartnerForm()
    if form.validate_on_submit():
        # Process form data
        contract = Contract(
            contract_title=form.contract_title.data,
            contract_description=form.contract_description.data,
            contract_no=form.contract_no.data,
            contract_form=form.contract_form.data,
            contract_status=form.contract_status.data,
            signed_date=form.signed_date.data,
            system_registered=form.system_registered.data,
            HQ_reported=form.HQ_reported.data,
            PIC_id=form.PIC_id.data,
            PIC_team=form.PIC_team.data
        )

        a_partner = Partner(
            partner_name = partner_form.partner_name,
            tax_no = partner_form.tax_no
        )
        
        # Save the contract to database
        db.session.add(contract, a_partner)
        db.session.commit()

        # Create a folder for the contract
        folder_name = f"{datetime.utcnow().strftime('%Y%m%d')}_{form.contract_form.data}_{form.contract_no.data}"
        folder_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # Save uploaded files
        for file in request.files.getlist('files'):
            if file and file.filename:
                filename = secure_filename(file.filename)
                save_path = os.path.join(folder_path, filename)
                file.save(save_path)
        
        flash("Contract successfully created!", "success")
        return redirect(url_for('route_main.new_contract'))

    return render_template('new_contract.html', form=form, partner_form=partner_form)

# Contract list route
@bp.route('/contract_list/', methods=['GET'])
def contract_list():
    page = request.args.get('page', 1, type=int)
    # contracts = Contract.query.paginate(page, 10, False)
    contracts = db.paginate(db.select(Contract).order_by(Contract.registration_date.desc()), page=page, per_page=10)
    return render_template('contract_list.html', contracts=contracts)

# Admin route for creating and dropping database
@bp.route('/temp_admin/', methods=['GET', 'POST'])
def temp_admin():
    if request.method == 'POST':
        if 'create_db' in request.form:
            db.create_all()
            flash("Database created!", "success")
        elif 'drop_db' in request.form:
            db.drop_all()
            flash("Database dropped!", "warning")
        return redirect(url_for('route_main.temp_admin'))

    return render_template('temp_admin.html')

@bp.route('/contract/<int:contract_id>', methods=['GET'])
def contract_details(contract_id):
    contract = db.session.get(Contract, contract_id)
    if not contract:
        flash("No contract found!", "warning")
        return redirect(url_for('route_main.contract_list'))
    form = ContractForm(obj=contract)
    return render_template('contract_details.html', contract=contract, form=form)

@bp.route('/contract/<int:contract_id>/update', methods=['POST'])
def update_contract(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    if not contract:
       flash("No contract found!", "warning")
       return redirect(url_for('route_main.contract_list'))
    form = ContractForm()
    if form.validate_on_submit():
        form.populate_obj(contract)
        db.session.commit()
        flash("Updated successfully!", "success")
    else:
        flash("Validation error", "warning" )
        for field, errors in form.errors.items():
            print(f"Field {field} has error: {errors}")
    return redirect(url_for('route_main.contract_list')) 