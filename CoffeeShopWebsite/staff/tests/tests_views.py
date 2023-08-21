from django.test import TestCase
from django.urls import reverse
from staff.models import CustomUserModel
from staff.forms import PhoneNumberForm, OtpForm
from coffeeshop.models import Footer


class LoginUserViewTest(TestCase):
    def setUp(self):
        self.url = reverse('staff:login')
        self.user = CustomUserModel.objects.create_user(
            phone_number='09123456789', password='Password@123',
            first_name='john', last_name='doe'
            )
        self.client.login(username='testuser', password='Password@123')
        self.footer = Footer.objects.create()

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertEqual(response.context['form1'], PhoneNumberForm)
        self.assertEqual(response.context['form2'], OtpForm)

    def test_post_form1_submit_valid(self):
        data = {'form1_submit': '', 'phone_number': '1234567890'}
        response = self.client.post(self.url, data)
        self.assertIsNotNone(self.client.session.get('phone_number'))
        self.assertEqual(response.status_code, 200)

    def test_post_form1_submit_invalid(self):
        data = {'form1_submit': '', 'phone_number': ''}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

    def test_post_form2_submit_valid(self):
        session = self.client.session
        session['phone_number'] = '1234567890'
        data = {'form2_submit': '', 'registration_code': '1234'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('coffeeshop:home'))

    def test_post_form2_submit_invalid(self):
        session = self.client.session
        session['phone_number'] = '1234567890'
        data = {'form2_submit': '', 'registration_code': ''}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
