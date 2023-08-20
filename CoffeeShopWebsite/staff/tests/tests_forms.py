from django.test import TestCase
from staff.forms import PhoneNumberForm, OtpForm

class FormsTestCase(TestCase):


    def test_phone_number_form(self):
        form_data = {'phone_number': '1234567890'}
        form = PhoneNumberForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_otp_form(self):
        form_data = {'registration_code': '1234'}
        form = OtpForm(data=form_data)
        self.assertTrue(form.is_valid())