from flask import jsonify, request, Response
from flask_login import login_required, current_user
from . import operations
from .. import db
from ..models import ContactDetail, ContactDetailSchema, contact_details_schema
from sqlalchemy import func

# route to create a new contact
@operations.route('/create', methods=['POST'])
@login_required
def insert_contact():
	if request.form.get('name') == None:
		resp = jsonify({'status':'failed', 'msg':'must supply name'})
		resp.status_code = 400
		return resp
	
	if request.form.get('email') == None:
		resp = jsonify({'status':'failed', 'msg':'must supply email'})
		resp.status_code = 400
		return resp

	if request.form.get('contact_number') == None:
		resp = jsonify({'status':'failed', 'msg':'must supply contact_number'})
		resp.status_code = 400
		return resp

	contact_details = ContactDetail( contact_number=request.form['contact_number'],
									 user_id=current_user.id, 
									 name=request.form['name'], 
									 email=request.form['email'],
									 created_timestamp = func.current_timestamp(),
									 last_modified_timestamp = func.current_timestamp()
									)
	try:
		db.session.add(contact_details)
		db.session.commit()
		resp = jsonify({'status':'ok', 'msg':'contact created'})
		resp.status_code = 200
		return resp
	## todo : catch specific exception
	except:
		resp = jsonify({'status':'failed', 'msg':'Email already exists'})
		resp.status_code = 409
		return resp

# route to edit an existing contact
@operations.route('/edit', methods=['PUT'])
@login_required
def edit_contact():
	if request.form.get('contact_id') == None:
		resp = jsonify({'status':'failed', 'msg':'must supply contact_id'})
		resp.status_code = 400
		return resp
	if request.form.get('name') == None:
		resp = jsonify({'status':'failed', 'msg':'must supply name'})
		resp.status_code = 400
		return resp		
	if request.form.get('contact_number') == None:
		resp = jsonify({'status':'failed', 'msg':'must supply contact_number'})
		resp.status_code = 400
		return resp		
	if request.form.get('email') == None:
		resp = jsonify({'status':'failed', 'msg':'must supply email'})
		resp.status_code = 400
		return resp		
	
	contact = ContactDetail.query.get_or_404(request.form['contact_id'])
	contact.name = request.form['name']
	contact.contact_number = request.form['contact_number']
	contact.email = request.form['email']
	contact.last_modified_timestamp = func.current_timestamp()
	try:
		db.session.commit()
		resp = jsonify({'status':'ok', 'msg':'updated successfully'})
		resp.status_code = 200
		return resp
	except:
		resp = jsonify({'status':'failed', 'msg':'Updated email address already exists'})
		resp.status_code = 409
		return resp

# route to delete an existing contact
@operations.route('/delete', methods=['DELETE'])
@login_required
def delete_contact():
	if request.form.get('contact_id') == None:
		resp = jsonify({'status':'failed', 'msg':'must supply contact_id'})
		resp.status_code = 400
		return resp		
	contact = ContactDetail.query.get_or_404(request.form['contact_id'])
	db.session.delete(contact)
	db.session.commit()
	resp = jsonify({'status':'ok', 'msg':'deleted successfully'})
	resp.status_code = 200
	return resp	

# route to search for contacts
@operations.route('/search', methods=['GET'])
@login_required
def search_contact():
	per_page = 10 if request.args.get('per_page') == None else int(request.args.get('per_page'))
	page = 1 if request.args.get('page') == None else int(request.args.get('page'))
	
	# searches contact just by name
	if 'name' in request.args and 'email' not in request.args:
		contact_list = contact_details_schema.dump(
			ContactDetail.query.filter_by(
				name=request.args.get('name')).paginate(page, per_page, False).items)
		if not contact_list.data:
			resp = jsonify({'status':'failed', 'msg':'not found', 'result':False})
			resp.status_code = 404
			return resp				
		resp = jsonify({'status':'ok', 'msg':'found', 'result':contact_list.data})
		resp.status_code = 200
		return resp	
	
	# searches contact just by email	
	if 'email' in request.args and 'name' not in request.args:
		contact_list = contact_details_schema.dump(
			ContactDetail.query.filter_by(
				email=request.args.get('email')).paginate(page, per_page, False).items)
		if not contact_list.data:
			resp = jsonify({'status':'failed', 'msg':'not found', 'result':False})
			resp.status_code = 404
			return resp				
		resp = jsonify({'status':'ok', 'msg':'found', 'result':contact_list.data})
		resp.status_code = 200
		return resp	
	
	# searches contact by both name and email
	if 'name' in request.args and 'email' in request.args:
		contact_list = contact_details_schema.dump(
			ContactDetail.query.filter_by(
				name=request.args.get('name'), 
				email=request.args.get('email')).paginate(page, per_page, False).items)
		if not contact_list.data:
			resp = jsonify({'status':'failed', 'msg':'not found','result':False})
			resp.status_code = 404
			return resp				
		resp = jsonify({'status':'ok', 'msg':'found', 'result':contact_list.data})
		resp.status_code = 200
		return resp	
	resp = jsonify({'status':'failed', 'msg':'name or email or both must be provided', 'result':False})
	resp.status_code = 400
	return resp		