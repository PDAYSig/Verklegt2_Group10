from django import forms


class CreditCardForm(forms.Form):
    CARD_CHOICES = (
    ('Visa', 'Visa'),
    ('Mastercard', 'Mastercard'),
    )
    card_type = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'}, choices=CARD_CHOICES))
    card_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    expiration_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
    cvc = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class BankTransferForm(forms.Form):
    iban = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class WireTransferForm(forms.Form):
    sending_bank = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    routing_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    account_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))