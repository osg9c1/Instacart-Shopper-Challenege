from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ApplicantAnalysisForm(forms.Form):
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}), label="Start Date")
    end_date = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}), label="End Date")


    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data['start_date']
        if end_date < start_date:
            raise ValidationError(_('End Date should be greater than Start Date'))
        else:
            return end_date


