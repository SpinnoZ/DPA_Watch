import os
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, current_app, send_file
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models import Contract, Partner, Audit
from .forms import ContractForm
from app.route_main import bp

# New contract route
@bp.route('/new_contract/', methods=['GET', 'POST'])
def new_contract():
    form = ContractForm()
    
    if form.validate_on_submit():
        # Process form data ===> TRY POPULATE AS OBJ
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
            partner_name = form.partner_name.data,
            tax_no = form.tax_no.data
        )
        
        print(a_partner.partner_name)
        print(a_partner.tax_no)
        db.session.add(contract, a_partner)
        contract.partner = a_partner
        
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
        
        contract.contract_folder = folder_name
        
        # Save the contract to database
        db.session.add(contract, a_partner)
        db.session.commit()
        
        flash("Contract successfully created!", "success")
    elif request.method == 'POST':
        flash("Validation error", "warning" )
        for field, errors in form.errors.items():
            print(f"Field {field} has error: {errors}")
            print(f"Contract Form is: {form.contract_form.data}")
            
            

    return render_template('new_contract.html', form=form)

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
        elif 'partners_populate' in request.form:
            for i in range(1, 21):
                partner = Partner(
                    partner_name=f"partner{i}",
                    tax_no=f"123{i}"
                )
                db.session.add(partner)

            db.session.commit()
            flash("Partners populated!", "success")
        return redirect(url_for('route_main.temp_admin'))

    return render_template('temp_admin.html')

@bp.route('/contract/<int:contract_id>', methods=['GET' ,'POST'])
def contract_details(contract_id):
    contract = db.session.get(Contract, contract_id)
    partner = db.session.get(Partner, contract.partner_id)
    if not contract:
        flash("No contract found!", "warning")
        return redirect(url_for('route_main.contract_list'))
    form = ContractForm(obj=contract)
    return render_template('contract_details.html', contract=contract, form=form)

@bp.route('/contract/<int:contract_id>/update', methods=['POST', 'GET'])
def update_contract(contract_id):
    
    contract = Contract.query.get_or_404(contract_id)
    form = ContractForm()
    if form.validate_on_submit():
        form.populate_obj(contract)
        

        # Save uploaded files
        for file in request.files.getlist('files'):
            if file and file.filename:
                filename = secure_filename(file.filename)
                save_path = os.path.join(os.path.join(current_app.config['UPLOAD_FOLDER'],contract.contract_folder), filename)
                file.save(save_path)
        
        db.session.commit()
        flash("Updated successfully!", "success")

    else:
        flash("Validation error", "warning" )
        for field, errors in form.errors.items():
            print(f"Field {field} has error: {errors}")
            print(f"Contract_Form is: {form.contract_form.data}")
            print(f"Firled Contract Status is: { form.contract_status.data}")
    return redirect(url_for('route_main.contract_list')) 

@bp.route('/filelist/<path:contract_folder>')
def file_list(contract_folder):
    full_contract_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], contract_folder)
    files = os.listdir(full_contract_folder)
    return render_template('file_list.html', files=files, contract_folder=contract_folder)

@bp.route('/download/<path:filename>')
def get_file(filename):
    filename = os.path.join(current_app.root_path, 'content/', filename)
    return send_file(filename, as_attachment=True)


# # # TEMP PARTNER PAGE

@bp.route("/choose_partner/")
def choose_partner():
    partners = Partner.query.all()
    partners_per_page = 10
    total_partners = Partner.query.count()
    total_pages = (total_partners + partners_per_page - 1) // partners_per_page  # Calculate total pages

    return render_template('temp_choose_partner.html', partners=partners, total_pages=total_pages, total_partners=total_partners)

# # # TEMP PARTNER AUTOCOMPLETE

@bp.route("/auto_partners/")
def auto_partners():
    partners = Partner.query.all()
    partners_list = []
    for partner in partners:
        partners_list.append(partner.partner_name)
    print(partners_list)
    return render_template('temp_partner_autocomplete.html', partners=partners_list)