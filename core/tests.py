import unittest
from datetime import datetime

from django.contrib.auth.models import User  # Assuming User model from django.contrib.auth
from pyhanko_certvalidator import ValidationError

from core.models import Patient


class PatientTest(unittest.TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.patient1 = Patient.objects.create(user=self.user)
        self.patient2 = Patient.objects.create(user=self.user, mobile='1234567890')
    def test_patient_creation(self):
        """
        Tests that a Patient object can be created successfully with valid data.
        """
        self.assertEqual(self.patient.user, self.user)
        self.assertIsNone(self.patient.mobile)  # Assuming mobile is initially null
        self.assertIsNone(self.patient.assignedDoctorId)  # Assuming assignedDoctorId is initially null
        self.assertTrue(self.patient.admitDate.isoformat() <= datetime.datetime.now().isoformat())
        self.assertTrue(self.patient.status)

    def test_get_name_property(self):
        """
        Tests that the get_name property returns the full name of the associated user.
        """
        self.user.first_name = 'John'
        self.user.last_name = 'Doe'
        self.user.save()  # Update the user object
        self.assertEqual(self.patient.get_name, 'John Doe')

    def test_get_id_property(self):
        """
        Tests that the get_id property returns the ID of the associated user.
        """
        self.assertEqual(self.patient.get_id, self.user.id)

    def test_invalid_mobile_length(self):
        """
        Tests that a validation error is raised for a mobile number exceeding the maximum length.
        """
        with self.assertRaises(ValidationError):
            self.patient.mobile = '12345678901234567890'  # Exceeds 20 characters
            self.patient.save()

    def test_invalid_assignedDoctorId(self):
        """
        Tests that a validation error is raised for a negative assignedDoctorId.
        """
        with self.assertRaises(ValidationError):
            self.patient.assignedDoctorId = -1
            self.patient.save()