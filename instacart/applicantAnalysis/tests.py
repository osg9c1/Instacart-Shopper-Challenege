from unittest import TestCase
from forms import ApplicantAnalysisForm
import datetime


class ApplicantAnalysisFormTest(TestCase):
    def test_form(self):
        start_date = datetime.datetime.today()
        end_date = start_date - datetime.timedelta(days=1)
        form = ApplicantAnalysisForm(data={'start_date': start_date, 'end_date': end_date})
        self.assertFalse(form.is_valid())
