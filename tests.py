import unittest
from flask_testing import TestCase
from app import db
from app.models import User, ContactDetail
from sqlalchemy import func
from app import create_app
from flask import url_for
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
        contact_detail = ContactDetail(name="test_contact_1", contact_number=9887889877, email='test1@gmail.com')
        
		# save user and contact to database
        db.session.add(user)
        db.session.add(contact_detail)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()


class TestModels(TestBase):
	def test_user_model(self):
        
		# create test user
		user = User(username='test_user_2', password='test_password_2')
		db.session.add(user)
		db.session.commit()
		self.assertEqual(User.query.count(), 2)
	
	def test_contact_detail_model(self):
		contact_details = ContactDetail( contact_number=9887889099,
									 user_id=12, 
									 name='test_contact_2', 
									 email='test2@gmail.com',
									 created_timestamp = func.current_timestamp(),
									 last_modified_timestamp = func.current_timestamp()
									)
		db.session.add(contact_details)
		db.session.commit()
		self.assertEqual(ContactDetail.query.count(), 2)


class TestViews(TestBase):
	
	def test_register_view(self):
		response = self.client.post('/register', data={'username':'reg_user', 'password':'reg_pass'})
		self.assertEquals(response.status_code, 200)

	def test_login_view(self):
		with self.client:
			self.client.post('/login', data={'username':'test_user_1', 'password':'test_password_1'})
			self.assertEquals(current_user.username, 'test_user_1')

	def test_create_view(self):
		with self.client:
			self.client.post('/login', data={'username':'test_user_1', 'password':'test_password_1'})
			response = self.client.post('/create', data={'name':'test_contact_3',
		 		'contact_number':9889887899, 'email':'test3@gmail.com'})
			self.assertEqual(response.status_code, 200)

	def test_search_view_with_name(self):
		with self.client:
			self.client.post('/login', data={'username':'test_user_1', 'password':'test_password_1'})
			response = self.client.get('/search?name=test_contact_1')
			self.assertEqual(response.status_code, 200)  
	
	def test_search_view_with_email(self):
		with self.client:
			self.client.post('/login', data={'username':'test_user_1', 'password':'test_password_1'})
			response = self.client.get('/search?email=test1@gmail.com')
			self.assertEqual(response.status_code, 200)  			

if __name__ == '__main__':
	unittest.main()	        