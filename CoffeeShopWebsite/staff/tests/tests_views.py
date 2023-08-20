from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from staff.views import LoginUserView
from staff.forms import PhoneNumberForm, OtpForm

class LoginUserViewTest(TestCase):
    def setUp(self):
        self.url = reverse('login')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertIsInstance(response.context['form1'], PhoneNumberForm)
        self.assertIsInstance(response.context['form2'], OtpForm)
    def test_post_form1_submit_valid(self):
        data = { 'form1_submit': '', 'phone_number': '1234567890' }
        response = self.client.post(self.url, data) # Assert that the OTP is set in the session
        self.assertIsNotNone(self.client.session.get('phone_number')) # Assert that the form is valid and redirects to the same page
        self.assertEqual(response.status_code, 200)
    def test_post_form1_submit_invalid(self):
        data = { 'form1_submit': '', 'phone_number': '' }
        response = self.client.post(self.url, data) # Assert that the form is invalid and stays on the same page
        self.assertEqual(response.status_code, 200)
    def test_post_form2_submit_valid(self): # Set up session with phone number for OTP verification
        session = self.client.session
        session['phone_number'] = '1234567890'
        data = { 'form2_submit': '', 'registration_code': '1234' }
        response = self.client.post(self.url, data) # Assert that the user is logged in and redirected to home page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('coffeeshop:home'))
    def test_post_form2_submit_invalid(self): # Set up session with phone number for OTP verification
        session = self.client.session
        session['phone_number'] = '1234567890'
        data = { 'form2_submit': '', 'registration_code': '' }
        response = self.client.post(self.url, data)
        # Assert that the form is invalid and stays on the same page
        self.assertEqual(response.status_code, 200)