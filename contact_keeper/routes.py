from flask import render_template, url_for, request, redirect, flash
from contact_keeper import application, db
from contact_keeper.forms import ContactForm, AddressForm
from contact_keeper.models import Contact, Address
from contact_keeper.helpers import get_primary_address

@application.route("/")
def contacts():
    contact_list = Contact.query.order_by(Contact.last_name)
    address_list = Address.query.all()
    # SQL equivalent
    # contact_list = db.session.execute("SELECT * FROM contact ORDER BY last_name")
    # address_list = db.session.execute("SELECT * FROM address")
    return render_template("contacts.html", contact_list=contact_list, address_list=address_list)

@application.route("/contact/<int:contact_id>")
def view_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    return render_template("view_contact.html", contact=contact)

@application.route("/contact/new", methods=['GET', 'POST'])
def add_contact():
    # Instantiate blank contact form
    form = ContactForm()
    legend = 'New Contact'
    cancel_target = 'contacts'
    contact_id = None
    if request.method == 'POST' and form.validate_on_submit():
        contact = Contact(first_name=form.first_name.data.title(), 
                          middle_name=form.middle_name.data.title(), 
                          last_name=form.last_name.data.title(), 
                          email=form.email.data,
                          phone=form.phone.data)
        # Error Handling
        try:
            db.session.add(contact)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding contact: {e}")
            flash(f'There was a problem adding the contact to the database', 'danger')
            return redirect(url_for('contacts'))
        flash(f'Contact created for {contact.first_name} {contact.middle_name} {contact.last_name}', 'success')
        return redirect(url_for('contacts'))
    # Error Handling
    elif request.method == 'POST':
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(f"{fieldName}: {err}")
        flash(f'There was a problem adding the contact to the database', 'danger')
        return redirect(url_for('contacts'))
    return render_template("contact_form.html", 
                           form=form, 
                           legend=legend, 
                           cancel_target=cancel_target, 
                           contact_id=contact_id)

@application.route("/contact/<int:contact_id>/update", methods=['GET', 'POST'])
def edit_contact(contact_id):
    # Retrieve contact
    contact = Contact.query.get_or_404(contact_id)
    # Instatiate contact form with prepopulated fields from contact
    form = ContactForm(obj=contact)
    legend='Edit Contact'
    cancel_target = 'view_contact'
    form.submit.label.text = 'Update Contact'
    if request.method == 'POST' and form.validate_on_submit():
        #update record values
        contact.first_name = form.first_name.data.title()
        contact.middle_name = form.middle_name.data.title()
        contact.last_name = form.last_name.data.title()
        contact.email = form.email.data
        contact.phone = form.phone.data
        # Error Handling
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding contact: {e}")
            flash(f'There was a problem adding the contact to the database', 'danger')
            return redirect(url_for('contacts'))
        flash(f'Update successful', 'success')
        return redirect(url_for('view_contact', contact_id=contact_id))
    # Error Handling
    elif request.method == 'POST':
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(f"{fieldName}: {err}")
        flash(f'There was a problem adding the contact to the database', 'danger')
        return redirect(url_for('contacts'))
    return render_template("contact_form.html", 
                           form=form, 
                           legend=legend, 
                           cancel_target=cancel_target, 
                           contact_id=contact_id)

@application.route("/contact/<int:contact_id>/delete", methods=['POST'])
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    # Delete addresses related to contact
    Address.query.filter_by(contact_id=contact_id).delete()
    db.session.delete(contact)
    db.session.commit()
    flash(f'Contact deleted', 'success')
    return redirect(url_for('contacts'))

@application.route("/address/<int:contact_id>/new", methods=['GET', 'POST'])
def add_address(contact_id):
    # Instantiate blank address form
    form = AddressForm(contact_id=contact_id)
    legend = 'New Address'
    cancel_target = 'view_contact'
    if request.method == 'POST' and form.validate_on_submit():
        # Handle primary swap
        primary_address = get_primary_address(contact_id)
        if primary_address['exists'] and form.is_primary.data:
            primary_address['record'].is_primary = False
        address = Address(street_1=form.street_1.data.title(), 
                          street_2=form.street_2.data.title(), 
                          city=form.city.data.title(), 
                          state=form.state.data,
                          zip=form.zip.data,
                          contact_id=form.contact_id.data,
                          is_primary=form.is_primary.data)
        db.session.add(address)
        db.session.commit()
        flash(f'Address created', 'success')
        return redirect(url_for('view_contact', contact_id=contact_id))
    # Error Handling
    elif request.method == 'POST':
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(f"{fieldName}: {err}")
        flash(f'There was a problem adding the contact to the database', 'danger')
        return redirect(url_for('view_contact', contact_id=contact_id))
    return render_template("address_form.html", 
                           form=form, 
                           contact_id=contact_id, 
                           legend=legend, 
                           cancel_target=cancel_target)

@application.route("/address/<int:address_id>/update", methods=['GET', 'POST'])
def edit_address(address_id):
    # Retrieve address
    address = Address.query.get_or_404(address_id)
    # Instatiate address form with prepopulated fields from address
    form = AddressForm(obj=address)
    legend='Edit Address'
    cancel_target = 'view_contact'
    form.submit.label.text = 'Update Address'
    primary_address = get_primary_address(address.contact_id)
    if request.method == 'POST' and form.validate_on_submit():
        # Handle primary swap
        if primary_address['exists'] and form.is_primary.data:
            primary_address['record'].is_primary = False
        #update record values
        address.street_1 = form.street_1.data.title()
        address.street_2 = form.street_2.data.title()
        address.city = form.city.data.title()
        address.state = form.state.data
        address.zip = form.zip.data
        address.is_primary = form.is_primary.data
        # Error Handling
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding address: {e}")
            flash(f'There was a problem editing the address', 'danger')
            return redirect(url_for('view_contact', contact_id=address.contact_id))
        flash(f'Update successful', 'success')
        return redirect(url_for('view_contact', contact_id=address.contact_id))
    # Error Handling
    elif request.method == 'POST':
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(f"{fieldName}: {err}")
        flash(f'There was a problem editing the address', 'danger')
        return redirect(url_for('view_contact', contact_id=address.contact_id))
    return render_template("address_form.html", 
                           form=form, 
                           is_primary=address.is_primary, 
                           contact_id=address.contact_id,
                           legend=legend,
                           cancel_target=cancel_target)

@application.route("/address/<int:address_id>/delete", methods=['POST'])
def delete_address(address_id):
    address = Address.query.get_or_404(address_id)
    db.session.delete(address)
    db.session.commit()
    flash(f'Address deleted', 'success')
    return redirect(url_for('contacts'))