from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Doctor, Patient

class YourAppTests(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_home_page(self):
        response = self.client.get(reverse('home-page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_admin_signup(self):
        # Assuming you have a URL named 'admin-signup'
        response = self.client.get(reverse('admin-signup'))
        self.assertEqual(response.status_code, 200)
        # You can add more assertions based on your specific view behavior

    # Add more tests for other views...

    def test_admin_dashboard_authenticated(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Assuming you have a URL named 'admin-dashboard'
        response = self.client.get(reverse('admin-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_dashboard.html')

    def test_admin_dashboard_unauthenticated(self):
        # Assuming you have a URL named 'admin-dashboard'
        response = self.client.get(reverse('admin-dashboard'))
        self.assertRedirects(response, '/login_user/?next=/admin-dashboard/')

    def tearDown(self):
        # Clean up any test data if needed
        pass
