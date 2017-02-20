from django import forms


class ShopperRegistrationForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Bruce'}), label="First Name")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Lee'}), label="Last Name")
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'bruce.lee@gmail.com'}), label="Email")
    phone_no = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
                                error_message=(
                                "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    zipcode = forms.RegexField(regex=r'^[0-9]{5}(?:-[0-9]{4})?$',
                               widget=forms.TextInput(attrs={'placeholder': '00000'}), label="Zipcode",
                               error_message=(
                               "ZipCode must be entered in the format: '99999'. Up to 5 digits allowed."))
    referral_code = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Optional'}),
                                    label="Referral Code")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")



class ShopperLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'bruce.lee@gmail.com'}), label="Email")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")