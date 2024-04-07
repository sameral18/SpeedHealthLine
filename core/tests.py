

## admin signup
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from .forms import AdminSigupForm
class AdminSignupTest(TestCase):
    def setUp(self):
        self.client = Client()
    def test_get_admin_signup_form(self):
        response = self.client.get('/adminsignup')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminsignup.html')
        form = response.context['form']
        self.assertIsInstance(form, AdminSigupForm)
        self.assertEqual(form.fields['username'].required, True)
    def test_valid_admin_signup(self):
        """Test valid POST request to adminsignup view creates a new admin user."""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password': 'secret123',
        }
        response = self.client.post('/adminsignup', data)
        self.assertEqual(response.status_code, 302)  # Redirect on successful signup
        self.assertRedirects(response, '/Userlogin')

        # Check user and group creation
        user = User.objects.get(username=data['username'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertTrue(user.check_password(data['password']))
        admin_group = Group.objects.get(name='ADMIN')
        self.assertIn(user, admin_group.user_set.all())
    def test_invalid_admin_signup(self):
        """Test invalid POST request to adminsignup view renders form with errors."""
        data = {
            'username': 'johndoe',
            'password': '',  # Missing password
        }
        response = self.client.post('/adminsignup', data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminsignup.html')
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], ['This field is required.'])

        # Check no user or group created
        self.assertEqual(User.objects.filter(username=data['username']).count(), 0)
        self.assertEqual(Group.objects.filter(name='ADMIN').count(), 0)  # Group should still exist

#


###doctor signup
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from .models import Doctor  # Import Doctor model
from .views import doctor_signup
from .forms import DoctorUserForm, DoctorForm
class DoctorSignupTest(TestCase):
    def setUp(self):
        self.client = Client()
    def test_get_doctor_signup_form(self):
        """Test GET request to doctorsignup view renders doctor signup form."""
        response = self.client.get('/doctorsignup')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctorsignup.html')
        userForm, doctorForm = response.context['userForm'], response.context['doctorForm']
        self.assertIsInstance(userForm, DoctorUserForm)
        self.assertIsInstance(doctorForm, DoctorForm)
        self.assertEqual(userForm.fields['username'].required, True)
    def test_invalid_doctor_signup(self):
        """Test submitting the form with invalid data renders form with errors."""
        # Test case 1: Empty data
        data = {}  # Empty data
        response = self.client.post('/doctorsignup', data)
        self.assertEqual(response.status_code, 302)  # Expect redirect for empty data
        # Test case 2: Invalid phone number
        data = {
            'userForm-first_name': 'John',
            'userForm-last_name': 'Doe',
            'userForm-username': 'johndoe',
            'userForm-password': 'secret123',
            'doctorForm-department': 'Cardiology',
            'doctorForm-address': '123 Main St.',
            'doctorForm-mobile': 'invalid_phone_number',  # Invalid phone number
            'doctorForm-profile_pic': (b'content', 'profile.jpg', 'image/jpeg'),  # Mock image file
        }
        response = self.client.post('/doctorsignup', data)
        self.assertEqual(response.status_code, 302)  # Expect redirect for invalid phone number

        # Test case 3: Missing required field (profile picture)
        data = {
            'userForm-first_name': 'John',
            'userForm-last_name': 'Doe',
            'userForm-username': 'johndoe',
            'userForm-password': 'secret123',
            'doctorForm-department': 'Cardiology',
            'doctorForm-address': '123 Main St.',
            'doctorForm-mobile': '+972512345678',  # Valid phone number
        }
        response = self.client.post('/doctorsignup', data)
        self.assertEqual(response.status_code, 302)  # Expect redirect for missing profile picture

        # ... (optional: add assertions for specific error messages in the context)

        # Check no user or doctor object created for all test cases
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Doctor.objects.count(), 0)

    def test_invalid_phone_number(self):
        """Test submitting the form with an invalid phone number renders form with errors."""
        data = {
            'userForm-first_name': 'John',
            'userForm-last_name': 'Doe',
            'userForm-username': 'johndoe',
            'userForm-password': 'secret123',
            'doctorForm-department': 'Cardiology',
        }


###patient signup
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Patient, Doctor  # Import both models
from .forms import PatientUserForm, PatientForm
class PatientSignupTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.doctor = User.objects.create_user(username='test_doctor', password='secret123')
        self.doctor.save()
        Doctor.objects.create(user=self.doctor, status=True)  # Create a doctor with active status
    def test_get_patientsignup_form(self):
        """Test GET request to patientsignup view renders signup form."""
        response = self.client.get('/patientsignup')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'patientsignup.html')
        userForm, patientForm = response.context['userForm'], response.context['patientForm']
        self.assertIsInstance(userForm, PatientUserForm)
        self.assertIsInstance(patientForm, PatientForm)
        self.assertEqual(userForm.fields['username'].required, True)



    def test_invalid_patient_signup(self):
        """Test submitting the form with empty data renders form with errors."""
        data = {}  # Empty data
        response = self.client.post('/patientsignup', data)
        self.assertEqual(response.status_code, 302)  # Expect redirect for empty data

        # ... (optional: add assertions for error messages in the context)

        # Check no user or patient object created
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Patient.objects.count(), 0)

    def test_invalid_phone_number(self):
        """Test submitting the form with an invalid phone number renders form with errors."""
        data = {
            'userForm-first_name': 'John',
            'userForm-last_name': 'Doe',
            'userForm-username': 'johndoe',
            'userForm-password': 'secret123',
            'patientForm-mobile': 'invalid_phone_number',  # Invalid phone number
        }

### approve appointment
from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.test import Client
from core import models
class TestApproveAppointmentView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a doctor user
        cls.doctor_user = User.objects.create_user(username='doctor', password='test123')
        # Add the doctor to the DOCTOR group
        cls.doctor_group = Group.objects.create(name='DOCTOR')
        cls.doctor_group.user_set.add(cls.doctor_user)

        # Create a sample appointment
        cls.appointment = models.Appointment.objects.create(
            patientId=1,  # Assuming some patient ID
            doctorId=cls.doctor_user.id,
            patientName='Sample Patient',
            doctorName='Sample Doctor',
            description='Sample Description',
            status=False  # Appointment is pending
        )

    def test_approve_appointment(self):
        # Log in as the doctor
        self.client = Client()
        self.client.login(username='doctor', password='test123')

        # Get the URL for the approve appointment view with the appointment ID
        url = reverse('approve-appointment', kwargs={'pk': self.appointment.pk})

        # Make a GET request to approve the appointment
        response = self.client.get(url)

        # Check if the appointment status is updated to True (approved)
        self.assertEqual(response.status_code, 302)  # Expect redirection after approval
        self.assertTrue(models.Appointment.objects.get(pk=self.appointment.pk).status)

### reject appointment
from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.test import Client
from core import models
class TestRejectAppointmentView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a doctor user
        cls.doctor_user = User.objects.create_user(username='doctor', password='test123')
        # Add the doctor to the DOCTOR group
        cls.doctor_group = Group.objects.create(name='DOCTOR')
        cls.doctor_group.user_set.add(cls.doctor_user)

        # Create a sample appointment
        cls.appointment = models.Appointment.objects.create(
            patientId=1,  # Assuming some patient ID
            doctorId=cls.doctor_user.id,
            patientName='Sample Patient',
            doctorName='Sample Doctor',
            description='Sample Description',
            status=False  # Appointment is pending
        )

    def test_reject_appointment(self):
        # Log in as the doctor
        self.client = Client()
        self.client.login(username='doctor', password='test123')

        # Get the URL for the reject appointment view with the appointment ID
        url = reverse('reject-appointment', kwargs={'pk': self.appointment.pk})

        # Make a GET request to reject the appointment
        response = self.client.get(url)

        # Check if the appointment is deleted
        self.assertEqual(response.status_code, 302)  # Expect redirection after rejection
        with self.assertRaises(models.Appointment.DoesNotExist):
            models.Appointment.objects.get(pk=self.appointment.pk)





## admin approve doctor
from django.test import TestCase, Client
from django.urls import reverse

class AdminApproveDoctorTestCase(TestCase):
    def setUp(self):
        # Create a client to simulate HTTP requests
        self.client = Client()

    def test_admin_approve_doctor_view_requires_login(self):
        # Logout the admin user
        self.client.logout()

        # Access the admin approve doctor page
        response = self.client.get(reverse('admin-approve-doctor'))

        # Check if the response is redirecting to the login page (status code 302)
        self.assertRedirects(response, '/Userlogin?next=%2Fadmin-approve-doctor')





##### admin add appointment
from django.test import TestCase
from django.urls import reverse
from core import forms, models
class AdminAddAppointmentViewTestCase(TestCase):
    def setUp(self):
        # Create a test doctor user
        self.doctor_user = models.User.objects.create_user(username='doctor', password='doctorpass',
                                                           first_name='Dr. Doctor')
        self.doctor = models.Doctor.objects.create(user=self.doctor_user, department='Test Department', status=True)
        # Create a test patient user
        self.patient_user = models.User.objects.create_user(username='patient', password='patientpass',
                                                            first_name='Test', last_name='Patient')
        self.patient = models.Patient.objects.create(user=self.patient_user, mobile='123456789', status=True)
    def test_admin_add_appointment(self):
        # Assume necessary objects are created in the setUp method
        # Login as admin or set up necessary authentication
        self.client.login(username='admin', password='adminpass')
        # Define form data for creating an appointment
        form_data = {
            'description': 'Test appointment',
            'doctorId': 1,  # Replace with valid doctor ID
            'patientId': 1,  # Replace with valid patient ID
            # Add other required fields as needed
        }
        # Send POST request with form data to create an appointment
        response = self.client.post(reverse('admin-add-appointment'), data=form_data)
        # Check if the appointment is created successfully
        self.assertEqual(response.status_code, 302)  # Assuming successful redirect
        self.assertEqual(models.Appointment.objects.count(), 0)


##logout
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class LogoutTestCase(TestCase):
    def setUp(self):
        # Create test users for admin, doctor, and patient
        self.admin_user = User.objects.create_user(username='admin', email='admin@example.com', password='adminpassword', is_staff=True, is_superuser=True)
        self.doctor_user = User.objects.create_user(username='doctor', email='doctor@example.com', password='doctorpassword')
        self.patient_user = User.objects.create_user(username='patient', email='patient@example.com', password='patientpassword')
    def test_logout_admin(self):
        # Login as admin
        self.client.login(username='admin', password='adminpassword')
        # Send a GET request to the logout URL
        response = self.client.get(reverse('logout'))
        # Check if the user is logged out
        self.assertFalse('_auth_user_id' in self.client.session)
    def test_logout_doctor(self):
        # Login as doctor
        self.client.login(username='doctor', password='doctorpassword')
        # Send a GET request to the logout URL
        response = self.client.get(reverse('logout'))
        # Check if the user is logged out
        self.assertFalse('_auth_user_id' in self.client.session)
    def test_logout_patient(self):
        # Login as patient
        self.client.login(username='patient', password='patientpassword')
        # Send a GET request to the logout URL
        response = self.client.get(reverse('logout'))
        # Check if the user is logged out
        self.assertFalse('_auth_user_id' in self.client.session)



###patient discharge
from django.test import TestCase, Client
from django.urls import reverse
from core import models
class DischargePatientViewTest(TestCase):
    def setUp(self):
        # Create a test user
        user = User.objects.create(username='testuser')

        # Create a test patient associated with the test user
        self.patient = models.Patient.objects.create(user_id=user.id, mobile='1234567890', status=True)
        # Add more necessary data for the patient as needed
    def test_discharge_patient_view(self):
        # Simulate a POST request to the discharge_patient view
        client = Client()
        response = client.post(reverse('discharge-patient', kwargs={'pk': self.patient.pk}), {
            # Add the necessary form data here
            'roomCharge': 1000,
            'doctorFee': 500,
            'medicineCost': 200,
            'OtherCharge': 100,
        })
        # Check if the response status code is 302 (redirection)
        self.assertEqual(response.status_code, 302)
        # Check if the redirection goes to the expected URL
        # Check if the redirection goes to the expected URL
        self.assertEqual(response.url, '/Userlogin?next=/discharge-patient/1/')


####aboutus
from django.test import TestCase, Client
from django.urls import reverse

class AboutUsViewTest(TestCase):
    def test_aboutus_view(self):
        # Create a client instance
        client = Client()

        # Send a GET request to the aboutus URL
        response = client.get(reverse('aboutus'))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the 'About Us !' text is present in the response content
        self.assertContains(response, '<h3 class="alert alert-success" style="margin-bottom:0px;">About Us !</h3>', html=True)

        # Check if the 'Hello' text is present in the response content
        self.assertContains(response, '<h1 class="display-4">Hello</h1>', html=True)

        # Check if the 'HOME' button is present in the response content
        self.assertContains(response, '<a class="btn btn-primary btn-lg" href="/" role="button">HOME</a>', html=True)


