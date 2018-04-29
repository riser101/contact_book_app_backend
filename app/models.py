from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager, ma

class User(UserMixin, db.Model):
	"""
	Creates a users table
	"""

	__tablename__ = 'users'
	id = db.Column(db.BigInteger, primary_key=True)
	username = db.Column(db.String(60), unique=True)
	password_hash = db.Column(db.String(128))

	@property
	def password(self):
		raise AttributeError('password should not be readable')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)
	# def __repr__(self):
	# 	return '<User: {}>'.format(self.email)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))	

class ContactDetail(db.Model):
	"""
	Creates a contact_details table
	"""		
	__tablename__ = 'contact_details'
	id = db.Column(db.BigInteger, primary_key=True)
	user_id = db.Column(db.BigInteger)
	name = db.Column(db.String(128))
	contact_number = db.Column(db.String(20))
	email = db.Column(db.String(128), unique=True)

	# def __repr__(self):
	# 	return '<Contact_details: {}>'.format(self.)

class ContactDetailSchema(ma.Schema):
	class Meta:
		fields = ('name', 'contact_number', 'email')		
		_links = ma.Hyperlinks({
        'self': ma.URLFor('user_detail', id='<id>'),
        'collection': ma.URLFor('users')
    })
contact_detail_schema = ContactDetailSchema()
contact_details_schema = ContactDetailSchema(many=True)		