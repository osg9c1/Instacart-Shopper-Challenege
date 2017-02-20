from django import forms


class ApplicantAnalysisForm(forms.Form):
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}), label="Start Date")
    end_date = forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}), label="End Date")


