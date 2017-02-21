from unittest import TestCase
from forms import ShopperRegistrationForm


class ShopperApplicantTests(TestCase):
    def test_shopper_applicant_valid_registration(self):
        first_name = "Sujata"
        last_name = "Mehta"
        email_id = "instacarttest2@gmail.com"
        phone_no = "234657983"
        zipcode = "86904"
        referral_code = "IN09"
        password = "test"
        form = ShopperRegistrationForm(data={'first_name': first_name, 'last_name': last_name, 'email': email_id,
                                             'phone_no': phone_no, 'zipcode': zipcode, 'referral_code': referral_code,
                                             'password': password})
        self.assertTrue(form.is_valid())

    def test_shopper_applicant_invalid_email(self):
        first_name = "Sujata"
        last_name = "Mehta"
        email_id = "instacarttest2"
        phone_no = "234657983"
        zipcode = "86904"
        referral_code = "IN09"
        password = "test"
        form = ShopperRegistrationForm(data={'first_name': first_name, 'last_name': last_name, 'email': email_id,
                                             'phone_no': phone_no, 'zipcode': zipcode, 'referral_code': referral_code,
                                             'password': password})
        self.assertFalse(form.is_valid())

    def test_shopper_applicant_invalid_zipcode(self):
        first_name = "Sujata"
        last_name = "Mehta"
        email_id = "instacarttest2@gmail.com"
        phone_no = "234657983"
        zipcode = "86904090090"
        referral_code = "IN09"
        password = "test"
        form = ShopperRegistrationForm(data={'first_name': first_name, 'last_name': last_name, 'email': email_id,
                                             'phone_no': phone_no, 'zipcode': zipcode, 'referral_code': referral_code,
                                             'password': password})
        self.assertFalse(form.is_valid())
