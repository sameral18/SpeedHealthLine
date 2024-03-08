from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Appointment
from datetime import datetime, date, timedelta

class AdminViewAppointmentTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create mock appointments (replace with actual data creation logic)
        self.appointment1 = Appointment.objects.create(
            doctorName="Dr. Smith",
            patientName="John Doe",
            description="Checkup",
            appointmentDate=date.today(),  # Use date from datetime module
            status=True  # Appointment with active status
        )
        self.appointment2 = Appointment.objects.create(
            doctorName="Dr. Jones",
            patientName="Jane Doe",
            description="Consultation",
            appointmentDate=date.today() + timedelta(days=1),
            status=False  # Appointment with inactive status (should not be retrieved)
        )

        # Simulate admin login (replace with your login logic)
        self.client.login(username='admin_user', password='admin_password')

    def test_admin_view_appointment_success(self):
        response = self.client.get(reverse('admin-view-appointment'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_view_appointment.html')

        # Check if appointments are present in the context
        self.assertIn(self.appointment1, response.context['appointments'])
        self.assertNotIn(self.appointment2, response.context['appointments'])

    def test_unauthorized_access(self):
        self.client.logout()
        response = self.client.get(reverse('admin-view-appointment'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
