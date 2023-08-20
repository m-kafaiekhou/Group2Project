from django.test import TestCase
from django.contrib.auth.models import User
from staff.manager import CustomUserManager

class CustomUserManagerTestCase(TestCase):


    def setUp(self):
        self.manager = CustomUserManager()

    def test_create_user(self):
        phone_number = '1234567890'
        first_name = 'John'
        last_name = 'Doe'
        password = 'password123'
        user = self.manager.create_user(phone_number, first_name, last_name, password)
        self.assertEqual(user.phone_number, phone_number)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        phone_number = '1234567890'
        first_name = 'John'
        last_name = 'Doe'
        password = 'password123'
        user = self.manager.create_superuser(phone_number, first_name, last_name, password)
        self.assertEqual(user.phone_number, phone_number)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
