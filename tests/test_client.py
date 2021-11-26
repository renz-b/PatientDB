import unittest
import re

from sqlalchemy.orm import query
from app import create_app, db
from app.models import Patient
from app.fake import patients

class FlaskClienttestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Hello!' in response.get_data(as_text=True))

    def test_404_page(self):
        response = self.client.get('/unknown')
        self.assertEqual(response.status_code, 404)

    def test_faker(self):
        patients()
        self.assertEqual(10, Patient.query.count())
    
    def test_model(self):
        response = Patient(first_name='test_name', last_name='test_lastname',
            middle_name='test_middlename', name_suffix='III', gender='m',
            birthday='2000-01-01', address='test_place', email_address='test@test.com',
            phone_number=66666)
        self.assertIsNotNone(response)
        self.assertEqual(response.first_name, 'test_name') 
        self.assertIsInstance(response, Patient)

    def test_add_patient_query_similar_patient_patient_details_and_delete(self):
        response = self.client.post('/commit_patient', data={
            'first_name' : 'test_name',
            'last_name' : 'test_lastname',
            'middle_name' : 'test_middlename',
            'name_suffix' : 'test',
            'gender' : 'm',
            'birthday' : '2000-01-01',
            'address' : 'test_place',
            'email_address' : 'test@test.com',
            'phone_number' : 666666,

            'hpi' : 'test_text',
            'pmh' : 'test_text',
            'fh' : 'test_text',
            'psh' : 'test_text',
            'obh' : 'test_text',
            'pe' : 'test_text'
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/similar_patient', data={
            'query' : 'true',
            'first_name' : 'test_name',
            'last_name' : 'test_lastname',
            'middle_name' : 'test_middlename',
            'address' : 'test_place',
            'gender' : 'm'
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/search', query_string={"query":"test_lastname"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(re.search('test_lastname', response.get_data(as_text=True)))

        response = self.client.get('/patient/1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(re.search('test_lastname', response.get_data(as_text=True)))

        response = self.client.get('/patient/delete_patient', query_string={"delete": 1})
        self.assertEqual(response.status_code, 302)

    def test_similar_patient_exception(self):
        response = self.client.post('/similar_patient', data={
            'query':'true'
        })
        self.assertEqual(response.status_code, 200)

        
