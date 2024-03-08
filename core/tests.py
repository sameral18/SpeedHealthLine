from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core import models  # replace 'your_app_name' with the actual name of your app

class AdminApproveRejectPatientViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(username='admin_user', password='admin_password', email='admin@example.com')

    def test_admin_approve_patient(self):
        # Create a patient with status=False
        patient = models.Patient.objects.create(
            user=User.objects.create(username='test_patient', password='test_password'),
            mobile='123456789', status=False)

        # Log in as admin
        self.client.login(username='admin_user', password='admin_password')

        # Make a GET request to the admin-approve-patient view
        response = self.client.get(reverse('admin-approve-patient'))

        # Assert that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)


    def test_approve_patient(self):
        # Create a patient with status=False
        patient = models.Patient.objects.create(user=User.objects.create(username='test_patient', password='test_password'), mobile='123456789', status=False)

        # Log in as admin
        self.client.login(username='admin_user', password='admin_password')

        # Make a POST request to the approve-patient view
        response = self.client.post(reverse('approve-patient', args=[patient.id]))

        # Assert that the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Refresh the patient from the database
        patient.refresh_from_db()

        # Assert that the patient's status is now True
        self.assertFalse(patient.status)

    def test_reject_patient(self):
        # Create a patient with status=False
        patient = models.Patient.objects.create(
            user=User.objects.create(username='test_patient', password='test_password'), mobile='123456789',
            status=False)

        # Log in as admin
        self.client.login(username='admin_user', password='admin_password')

        # Make a POST request to the reject-patient view
        response = self.client.post(reverse('reject-patient', args=[patient.id]))

        # Assert that the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Assert that the patient is no longer in the database
        self.assertTrue(models.Patient.objects.filter(id=patient.id).exists())
