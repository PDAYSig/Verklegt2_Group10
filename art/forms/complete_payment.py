from django.forms import ModelForm
from django_countries.fields import CountryField
from django import forms
from art.models import Sale
class CompletePaymentForm(forms.ModelForm):
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    street = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    postal_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = CountryField()
    class Meta:
        model = Sale
        exclude = ['id', 'seller', 'buyer', 'listing']
        widgets = {
            'buyer_billing_address' : forms.TextInput(attrs={'class': 'form-control'}),
            'payment_method' : forms.Select(attrs={'class': 'form-control'}),
        }
