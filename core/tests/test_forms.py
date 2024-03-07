from django.test import TestCase
from django.contrib.auth.models import User
from core.forms import AdminSigupForm, DoctorUserForm, DoctorForm, PatientUserForm, PatientForm, AppointmentForm, \
    PatientAppointmentForm, ContactusForm
from core.models import Doctor, Patient, Appointment
from django.test import TestCase



class FormsTestCase(TestCase):
    def test_admin_signup_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'john_doe',
            'password': 'securepassword',
        }
        form = AdminSigupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_doctor_user_form(self):
        form_data = {
            'first_name': 'Doctor',
            'last_name': 'User',
            'username': 'doctor_user',
            'password': 'securepassword',
        }
        form = DoctorUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Add similar tests for other forms...

    def test_contact_us_form(self):
        form_data = {
            'Name': 'John Doe',
            'Email': 'john@example.com',
            'Message': 'This is a test message.',
        }
        form = ContactusForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Add more tests for other forms...

    def test_appointment_form(self):
        doctor = Doctor.objects.create(first_name='Dr. Test', last_name='Doctor', username='dr_test',
                                       password='securepassword')
        patient = Patient.objects.create(first_name='Test', last_name='Patient', username='test_patient',
                                         password='securepassword')

        form_data = {
            'description': 'Test appointment',
            'status': 'scheduled',
            'doctorId': doctor.user_id,
            'patientId': patient.user_id,
        }
        form = AppointmentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_patient_appointment_form(self):
        doctor = Doctor.objects.create(first_name='Dr. Test', last_name='Doctor', username='dr_test',
                                       password='securepassword')

        form_data = {
            'description': 'Test appointment',
            'status': 'scheduled',
            'doctorId': doctor.user_id,
        }
        form = PatientAppointmentForm(data=form_data)
        self.assertTrue(form.is_valid())
