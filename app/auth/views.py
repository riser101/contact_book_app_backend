from flask import jsonify, request, Response
from flask_login import login_required, login_user, logout_user
from . import auth
from .. import db
from ..models import User
from sqlalchemy import func, exc

@auth.route('/register', methods=['POST'])
def register():
    """
    Handle requests to the /register route
    Add an user to the database through the registration api
    """	
    if request.form.get('username') == None:
    	resp = jsonify({'status':'failed', 'msg':'must supply username'})
    	resp.status_code = 400
    	return resp

    if request.form.get('password') == None:
    	resp = jsonify({'status':'failed', 'msg':'must supply password'})
    	resp.status_code = 400
    	return resp

    username = str(request.form.get('username'))
    password = str(request.form.get('password'))
    user = User(username=username, password=password, created_timestamp=func.current_timestamp(),
        last_modified_timestamp = func.current_timestamp())
    db.session.add(user)
    try:
    	db.session.commit()
    except exc.IntegrityError: 
		resp = jsonify({'status':'failed', 'msg':'username already exists'})
		resp.status_code = 400
		return resp    		
    resp = jsonify({'status':'ok', 'msg':'user created successfully'})
    resp.status_code = 200
    return resp         

# route to login a user into the application
@auth.route('/login', methods=['POST'])
def login():
    """
    Handle requests to the /login route
    logs-in a user to the app
    """ 
    if request.form.get('username') == None:
        resp = jsonify({'status':'failed', 'msg':'must supply username'})
        resp.status_code = 400
        return resp

    if request.form.get('password') == None:
        resp = jsonify({'status':'failed', 'msg':'must supply password'})
        resp.status_code = 400
        return resp

    username = str(request.form['username'])
    password = str(request.form['password'])
    user = User.query.filter_by(username=username).first()
    if user is not None and user.verify_password(password):
        login_user(user)
        resp = jsonify({'status':'ok', 'msg':'logged-in successfully'})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({'status':'failed', 'msg':'incorrect login credentials'})
        resp.status_code = 401
        return resp