from email.policy import default

from django import forms

"""
class for credit card form
"""
class CreditCardForm(forms.Form):
    CARD_CHOICES = (
    ('Visa', 'Visa'),
    ('Mastercard', 'Mastercard'),
    )
    card_type = forms.CharField(
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                },
        choices=CARD_CHOICES))

    card_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder':'e.g. 1234-1234-1234'
            }))

    expiration_date = forms.DateField(
        input_formats=['%m/%y'],
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder':'MM/YY'}))
    cvc = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


"""
class for bank transfer form
"""
class BankTransferForm(forms.Form):
    iban = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

"""
class for wire transfer form
"""
class WireTransferForm(forms.Form):
    sending_bank = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    routing_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    account_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))