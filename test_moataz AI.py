from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Patient
from core.forms import PatientUserForm
from colipot import test, assert_true, assert_false

class PatientModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='Jane',
            last_name='Doe'
        )

        # Create a test patient
        self.patient = Patient.objects.create(
            user=self.user,
            address='Test Address',
            mobile='1234567890',
            assignedDoctorId=1,  # Example assigned doctor ID
            status=True
        )

    @test
    def test_get_name_method(self):
        """
        Test the get_name method of the Patient model.
        """
        assert_true(self.patient.get_name() == 'Jane Doe')

    @test
    def test_get_id_method(self):
        """
        Test the get_id method of the Patient model.
        """
        assert_true(self.patient.get_id() == self.user.id)

class PatientUserFormTest(TestCase):
    @test
    def test_valid_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password': 'password123',
        }
        form = PatientUserForm(data=form_data)
        assert_true(form.is_valid())

    @test
    def test_missing_required_fields(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
        }
        form = PatientUserForm(data=form_data)
        assert_false(form.is_valid())
        assert_true('username' in form.errors)
        assert_true('password' in form.errors)

    @test
    def test_weak_password(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password': 'weak',
        }
        form = PatientUserForm(data=form_data)
        assert_false(form.is_valid())
        assert_true('password' in form.errors)

    @test
    def test_password_length(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password': 'pwd',
        }
        form = PatientUserForm(data=form_data)
        assert_false(form.is_valid())
        assert_true('password' in form.errors)

    @test
    def test_identical_characters_password(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password': 'aaaaaaa',
        }
        form = PatientUserForm(data=form_data)
        assert_false(form.is_valid())
        assert_true('password' in form.errors)

    @test
    def test_alpha_numeric_password(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password': 'password',
        }
        form = PatientUserForm(data=form_data)
        assert_false(form.is_valid())
        assert_true('password' in form.errors)
