from django.test import TestCase
from django.urls import reverse
from .models import User

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='normaluser', password='password123', email='test@test.com', role='driver')
        self.assertEqual(user.username, 'normaluser')
        self.assertEqual(user.role, 'driver')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(username='super', password='password123', email='super@test.com')
        admin.role = 'admin'
        admin.save()
        self.assertEqual(admin.username, 'super')
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.role, 'admin')

class AccountsViewTest(TestCase):
    def test_register_view(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_login_view(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
