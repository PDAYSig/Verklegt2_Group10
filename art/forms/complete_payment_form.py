from django_countries.fields import CountryField
from django import forms
from art.models import Sale

"""
class for the form of completing a payment with every info which is needed to do that
"""
class CompletePaymentForm(forms.ModelForm):
    buyer_country = CountryField(blank_label='Select Country').formfield()
    class Meta:
        model = Sale
        exclude = ['id', 'seller', 'buyer', 'listing']
        widgets = {
            'buyer_nid': forms.TextInput(attrs={'class': 'form-control'}),
            'buyer_city' : forms.TextInput(attrs={'class': 'form-control'}),
            'buyer_street' : forms.TextInput(attrs={'class': 'form-control'}),
            'buyer_postal_code' : forms.TextInput(attrs={'class': 'form-control'}),
            'payment_method' : forms.Select(attrs={'class': 'form-control'}),
            'national_id' : forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),min_length=10, max_length=10),
        }
