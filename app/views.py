# views.py
from flask import session, request, jsonify
from flask_login import login_required, login_user, current_user
from app import app, db
from .models import User, ContactDetail, ContactDetailSchema, contact_details_schema
import json

# route to login a user into the application
@app.route('/api/login', methods=['POST'])
def login():
    username = str(request.form['username'])
    password = str(request.form['password'])
    user = User.query.filter_by(username=username).first()
    if user is not None and user.verify_password(password):
    	login_user(user)
    	return 'success, you are logged in'
    else:
    	return 'Failed. username or password is wrong'
    
# route to create a new contact
@app.route('/api/create', methods=['POST'])
@login_required
def insert_contact():
	contact_details = ContactDetail(contact_number=request.form['contact_number'],
									user_id=current_user.id, 
									name=request.form['name'], 
									email=request.form['email'])
	try:
		db.session.add(contact_details)
		db.session.commit()
		return 'Contact created successfully'
	except:
		return 'Given email address already exists'
	
# route to edit an existing contact
@app.route('/api/edit', methods=['PUT'])
@login_required
def edit_contact():
	contact = ContactDetail.query.get_or_404(request.form['contact_id'])
	contact.name = request.form['last']
	contact.contact_number = request.form['contact_number']
	contact.email = request.form['email']
	try:
		db.session.commit()
		return 'Contact updated'	
	except:
		return 'Updated email address already exists'

# route to delete an existing contact
@app.route('/api/delete', methods=['DELETE'])
@login_required
def delete_contact():
	contact = ContactDetail.query.get_or_404(request.form['contact_id'])
	db.session.delete(contact)
	db.session.commit()
	return 'Contact deleted successfully'	

# route to search for contacts
@app.route('/api/search', methods=['GET'])
@login_required
def search_contact():
	per_page = 10 if request.args.get('per_page') == None else int(request.args.get('per_page'))
	page = 1 if request.args.get('page') == None else int(request.args.get('page'))
	
	if 'name' in request.args and 'email' not in request.args:
		contact_list = contact_details_schema.dump(
			ContactDetail.query.filter_by(
				name=request.args.get('name')).paginate(page, per_page, False).items)
		if not contact_list.data:
			return 'No contact with the given details'
		return jsonify(contact_list.data)

	if 'email' in request.args and 'name' not in request.args:
		contact_list = contact_details_schema.dump(
			ContactDetail.query.filter_by(
				email=request.args.get('email')).paginate(page, per_page, False).items)
		if not contact_list.data:
			return 'No contact with the given details'
		return jsonify(contact_list.data)

	if 'name' in request.args and 'email' in request.args:
		contact_list = contact_details_schema.dump(
			ContactDetail.query.filter_by(
				name=request.args.get('name'), 
				email=request.args.get('email')).paginate(page, per_page, False).items)
		if not contact_list.data:
			return 'No contact with the given details'
		return jsonify(contact_list.data)

	return 'Either name or email must be provided'	

# creates a brand new user
    # user = User(username='disha', password='hashme')
    # db.session.add(user)
    # db.session.commit()
    # return 'success'