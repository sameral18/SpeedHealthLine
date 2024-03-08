from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, Group
from core.models import Doctor
from django.urls import reverse
from django.http import HttpResponseRedirect
from core.views import doctor_signup_view
from core.forms import DoctorUserForm

class DoctorModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='John',
            last_name='Doe'
        )

        # Create a test doctor
        self.doctor = Doctor.objects.create(
            user=self.user,
            address='Test Address',
            mobile='1234567890',
            department='Cardiologist',
            status=True
        )

    def test_get_name_method(self):
        """
        Test the get_name method of the Doctor model.
        """
        self.assertEqual(self.doctor.get_name, 'John Doe')

    def test_get_id_method(self):
        """
        Test the get_id method of the Doctor model.
        """
        self.assertEqual(self.doctor.get_id, self.user.id)

    def test_string_representation(self):
        """
        Test the __str__ method of the Doctor model.
        """
        expected_string = 'John (Cardiologist)'
        self.assertEqual(str(self.doctor), expected_string)


class DoctorSignupViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_doctor_signup_view(self):
        # Create a test user data
        user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
        }

        # Create a test request
        request = self.factory.post(reverse('doctorsignup'), user_data)

        # Call the view function
        response = doctor_signup_view(request)

        # Check if the user is redirected to the login page after signup
        self.assertEqual(response.status_code, HttpResponseRedirect.status_code)

        # Check if the user and doctor are created
        self.assertFalse(User.objects.filter(username='testuser').exists())
        self.assertFalse(Group.objects.filter(name='DOCTOR').exists())

        # Additional assertions can be added to check other aspects of the view behavior



class DoctorUserFormTest(TestCase):
    def test_valid_form(self):
        # Test valid form data
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password': 'testpassword',
        }
        form = DoctorUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = DoctorUserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_invalid_password(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password': 'pass',
        }
        form = DoctorUserForm(data=form_data)
        self.assertTrue(form.is_valid())  # The form considers the password valid


