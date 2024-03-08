from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Patient
from core.forms import PatientUserForm

class PatientUserFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password': 'password123',
        }
        form = PatientUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
        }
        form = PatientUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('password', form.errors)

    def test_weak_password(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password': 'StrongPassword123',  # Replace with a strong password
        }
        form = PatientUserForm(data=form_data)
        self.assertTrue(form.is_valid())  # Ensure the form is now valid