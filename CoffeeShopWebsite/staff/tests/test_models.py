from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from staff.models import CustomUserModel


class CustomUserModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserModel.objects.create(
            phone_number='09123456787',
            first_name='John', last_name='Doe',
            password='Test123@',
            is_staff=True, is_active=True
        )

    def test_phone_number_validation(self):
        self.user.phone_number = '09123456787'
        self.user.full_clean()
        with self.assertRaises(ValidationError):
            self.user.phone_number = '1234567890'
            self.user.full_clean()

    def test_str_representation(self):
        expected_str = '09123456787'
        self.assertEqual(str(self.user), expected_str)

    def test_default_values(self):
        now = timezone.now()
        user = CustomUserModel.objects.create(phone_number='0987654321')
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.date_added.date(), now.date())

    # def test_required_fields(self):
    #     required_fields = ['phone_number', 'password']
    #     for field in required_fields:
    #         with self.assertRaises(ValidationError) as cm:
    #             setattr(self.user, field, '')
    #             self.user.full_clean()
    #         exception_message = str(cm.exception)
    #         expected_message = f'{field.capitalize()} cannot be blank.'
    #         self.assertEqual(exception_message, expected_message)
