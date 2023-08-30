# from django.test import TestCase
# from staff.models import CustomUserModel
# from coffeeshop.models import Footer
# from staff.backends import CustomUserBackend
# from django.contrib.auth.models import Group
#
#
# class CustomUserBackendTest(TestCase):
#     def setUp(self):
#         self.user = CustomUserModel.objects.create_user(
#             phone_number='1234567890', password='testpassword',
#             first_name='john', last_name='doe'
#         )
#         self.group = Group.objects.create()
#         self.footer = Footer.objects.create()
#
#     def test_authenticate_with_valid_credentials(self):
#         request = self.client.request().wsgi_request
#         request.session = {'otp': {'code': '1234', 'str_expire_time': '2030-01-01 00:00:00'}, 'phone_number': '1234567890'}
#         backend = CustomUserBackend()
#         user = backend.authenticate(request, phone_number='1234567890', otp_code='1234')
#         self.assertEqual(user, self.user)
#
#     def test_authenticate_with_invalid_otp_code(self):
#         request = self.client.request().wsgi_request
#         request.session = {'otp': {'code': '1234', 'str_expire_time': '2030-01-01 00:00:00'}, 'phone_number': '1234567890'}
#         backend = CustomUserBackend()
#         user = backend.authenticate(request, phone_number='1234567890', otp_code='5678')
#         self.assertIsNone(user)
#
#     def test_authenticate_with_expired_otp_code(self):
#         request = self.client.request().wsgi_request
#         request.session = {'otp': {'code': '1234', 'str_expire_time': '2000-01-01 00:00:00'}, 'phone_number': '1234567890'}
#         backend = CustomUserBackend()
#         user = backend.authenticate(request, phone_number='1234567890', otp_code='1234')
#         self.assertIsNone(user)
#
#     def test_phone_number_not_provided(self):
#         request = self.client.request().wsgi_request
#         backend = CustomUserBackend()
#         user = backend.authenticate(request, phone_number=None, otp_code=None)
#         self.assertIsNone(user)
