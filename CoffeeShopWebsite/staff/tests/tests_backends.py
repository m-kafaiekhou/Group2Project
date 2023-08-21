import datetime
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import get_object_or_404
from django.test import TestCase
from staff.models import CustomUserModel


class CustomUserBackendTest(TestCase):
    def setUp(self):
        self.user = CustomUserModel.objects.create_user(phone_number='1234567890', password='testpassword')

    def test_authenticate_with_valid_credentials(self):
        request = self.client.request().wsgi_request
        request.session = {'otp': {'code': '1234', 'str_expire_time': '2022-01-01 00:00:00'}, 'phone_number': '1234567890'}
        backend = CustomUserBackend()
        user = backend.authenticate(request, phone_number='1234567890', otp_code='1234')
        self.assertEqual(user, self.user)

    def test_authenticate_with_invalid_otp_code(self):
        request = self.client.request().wsgi_request
        request.session = {'otp': {'code': '1234', 'str_expire_time': '2022-01-01 00:00:00'}, 'phone_number': '1234567890'}
        backend = CustomUserBackend()
        user = backend.authenticate(request, phone_number='1234567890', otp_code='5678')
        self.assertIsNone(user)

    def test_authenticate_with_expired_otp_code(self):
        request = self.client.request().wsgi_request
        request.session = {'otp': {'code': '1234', 'str_expire_time': '2000-01-01 00:00:00'}, 'phone_number': '1234567890'}
        backend = CustomUserBackend()
        user = backend.authenticate(request, phone_number='1234567890', otp_code='1234')
        self.assertIsNone(user)
        self.assertMessageCount(messages.ERROR, 1)
