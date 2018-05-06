import unittest
from flask_testing import TestCase
from app import db
from app.models import User, ContactDetail
from sqlalchemy import func
from app import create_app
from flask import current_app
from flask_login import current_user


class TestBase(TestCase):

    def create_app(self):
		# pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql://contact_app_admin:bk9106@localhost/contact_app_db_test'
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        db.create_all()
		# create test first user
        user = User(username="test_user_1", password="test_password_1")
        first_contact = ContactDetail(name="test_contact_1", contact_number='+919887889877', email='test1@gmail.com')
        second_contact = ContactDetail(name="test_contact_2", contact_number='+919887889879', email='abc@gmail.com')
        # save user and contact to database
        db.session.add(user)
        db.session.add(first_contact)
        db.session.add(second_contact)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """
        db.session.remove()
        db.drop_all()

class BasicsTestCase(TestBase):
	def test_app_exists(self):
		self.assertFalse(current_app is None)

	def test_app_is_testing(self):
		self.assertTrue(current_app.config['TESTING'])


class TestModels(TestBase):
	def test_user_model(self):
        
		# create test user
		user = User(username='test_user_2', password='test_password_2')
		db.session.add(user)
		db.session.commit()
		self.assertEqual(User.query.count(), 2)
	
	def test_contact_detail_model(self):
		# creates test contact 
		contact_details = ContactDetail( contact_number='+919887889099', user_id=1, name='test_contact_2',
			email='test2@gmail.com', created_timestamp = func.current_timestamp(),
			last_modified_timestamp = func.current_timestamp()
									)
		db.session.add(contact_details)
		db.session.commit()
		self.assertEqual(ContactDetail.query.count(), 3)
    
	def test_password_setter(self):
		u = User(password='password')
		self.assertTrue(u.password_hash is not None)		

	def test_no_password_getter(self):
		u = User(password='password')
		with self.assertRaises(AttributeError):
			u.password()		

	def test_password_verification(self):
		u = User(password='password')
		self.assertTrue(u.verify_password('password'))
		self.assertFalse(u.verify_password('notpassword'))

	def test_password_salts_are_random(self):
		u1 = User(password='password')
		u2 = User(password='password')
		self.assertTrue(u1.password_hash != u2.password_hash)		

class TestViews(TestBase):
	def test_register_view(self):
		response = self.client.post('/register', data={'username':'reg_user', 'password':'reg_pass'})
		self.assertEquals(response.status_code, 200)
		
		# no password provided
		response = self.client.post('/register', data={'username':'reg_user'})
		self.assertEquals(response.status_code, 400)
		
		# no user provided
		response = self.client.post('/register', data={'password':'reg_pass'})
		self.assertEquals(response.status_code, 400)		
		
		# no params provided
		response = self.client.post('/register')
		self.assertEquals(response.status_code, 400)
		
		# user already exists, raises integrity exception
		response = self.client.post('/register', data={'username':'reg_user', 'password':'reg_pass'})
		self.assertEquals(response.status_code, 400)				


	def test_login_view(self):
		response = self.client.post('/login', data={'username':'test_user_1', 'password':'test_password_1'})
		self.assertEquals(response.status_code, 200)
		
		# wrong credentials validation
		response = self.client.post('/login', data={'username':'wrong_user', 'password':'wrong_password'})
		self.assertEquals(response.status_code, 401)
		
		# no password provided
		response = self.client.post('/login', data={'username':'test_user_1'})
		self.assertEquals(response.status_code, 400)
		
		# no user provided
		response = self.client.post('/login', data={'password':'test_password_1'})
		self.assertEquals(response.status_code, 400)		
		
		# no params provided
		response = self.client.post('/login')
		self.assertEquals(response.status_code, 400)
		
	def test_create_view(self):
		with self.client:
			
			self.client.post('/login', data={'username':'test_user_1', 'password':'test_password_1'})
			response = self.client.post('/create', data={'name':'test_contact_3',
		 		'contact_number':'+919889887899', 'email':'test3@gmail.com'})
			self.assertEqual(response.status_code, 200)
			
			# no name param error
			response = self.client.post('/create', data={'contact_number':'+919889887899', 'email':'test3@gmail.com'})
			self.assertEqual(response.status_code, 400)
			
			# no contact_number param error
			response = self.client.post('/create', data={'name':'test_contact_3', 'email':'test3@gmail.com'})
			self.assertEqual(response.status_code, 400)			
			
			# no email param error
			response = self.client.post('/create', data={'name':'test_contact_3',
		 		'contact_number':'+919889887899'})
			self.assertEqual(response.status_code, 400)			

			# invalid contact_number error
			response = self.client.post('/create', data={'name':'test_contact_3',
		 		'contact_number':'+9197899', 'email':'test3@gmail.com'})
			self.assertEqual(response.status_code, 400)			

			# no country code error in contact_number or invalid email
			response = self.client.post('/create', data={'name':'test_contact_3',
		 		'contact_number':'+9881880422', 'email':'test3gmail.com'})
			self.assertEqual(response.status_code, 400)						

		    # duplicate email/contact number error
			response = self.client.post('/create', data={'name':'test_contact_3',
		 		'contact_number':'+919889887899', 'email':'test3@gmail.com'})
			self.assertEqual(response.status_code, 409)						


	def test_search_view_with_name(self):
		with self.client:
			
			self.client.post('/login', data={'username':'test_user_1', 'password':'test_password_1'})
			response = self.client.get('/search?name=test_contact_1')
			self.assertEqual(response.status_code, 200)
			
			# name not found error
			response = self.client.get('/search?name=random_name')
			self.assertEqual(response.status_code, 404)
			
			#atleast name or email error  
			response = self.client.get('/search')
			self.assertEqual(response.status_code, 400)
	
	def test_search_view_with_email(self):
		with self.client:
			self.client.post('/login', data={'username':'test_user_1', 'password':'test_password_1'})
			response = self.client.get('/search?email=test1@gmail.com')
			self.assertEqual(response.status_code, 200)
			
			# email not found error
			response = self.client.get('/search?email=random@gmail.com')
			self.assertEqual(response.status_code, 404)    

	def test_search_view_with_name_and_email(self):
		with self.client:
			self.client.post('/login', data={'username':'test_user_1', 'password':'test_password_1'})
			response = self.client.get('/search?name=test_contact_1&email=test1@gmail.com')
			self.assertEqual(response.status_code, 200)

			# contact does not exists error
			response = self.client.get('/search?name=not_exists&email=not_exists@gmail.com')
			self.assertEqual(response.status_code, 404)  		  		

	def test_edit_view(self):
		with self.client:
			self.client.post('/login', data={'username':'test_user_1', 'password':'test_password_1'})
			response = self.client.put('/edit', data={'contact_id':1, 'name':'updated_name',
				 'contact_number':'+919887887677', 'email':'edit_test@gmail.com'})
			self.assertEqual(response.status_code, 200)
			
			# duplicate contact error
			response = self.client.put('/edit', data={'contact_id':2, 'name':'updated_name',
				 'contact_number':'+919887887677', 'email':'edit_test@gmail.com'})
			self.assertEqual(response.status_code, 409)			
			
			# contact param validation error
			response = self.client.put('/edit', data={'name':'updated_name',
				 'contact_number':'+919887887677', 'email':'edit_test@gmail.com'})
			self.assertEqual(response.status_code, 400)
			
			# name param validation error
			response = self.client.put('/edit', data={'contact_id':1, 'contact_number':'+919887887677', 
				'email':'edit_test@gmail.com'})
			self.assertEqual(response.status_code, 400)
			
			# contact_number param validation error
			response = self.client.put('/edit', data={'contact_id':1, 'name':'updated_name', 
				'email':'edit_test@gmail.com'})
			self.assertEqual(response.status_code, 400)
			
			# email param validation error
			response = self.client.put('/edit', data={'contact_id':1, 'name':'updated_name',
				 'contact_number':'+919887887677'})
			self.assertEqual(response.status_code, 400)

	def test_delete_view(self):
		with self.client:
			self.client.post('/login', data={'username':'test_user_1', 'password':'test_password_1'})
			response = self.client.delete('/delete', data={'contact_id':1})
			self.assertEqual(response.status_code, 200)			
			
			# contact_id param validation error
			response = self.client.delete('/delete')
			self.assertEqual(response.status_code, 400)			

if __name__ == '__main__':
	unittest.main()	        