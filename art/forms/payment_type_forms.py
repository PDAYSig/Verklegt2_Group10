from django import forms

class CreditCardForm(forms.Form):
    """
    class for credit card form
    """
    CARD_CHOICES = (
    ('Visa', 'Visa'),
    ('Mastercard', 'Mastercard'),
    )
    card_type = forms.CharField(
        widget=forms.Select(
            attrs={
                'class': 'form-control-c',
                },
        choices=CARD_CHOICES))

    card_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control-c',
                'placeholder':'e.g. 1234-1234-1234'
            }))

    expiration_date = forms.DateField(
        input_formats=['%m/%y'],
        widget=forms.DateInput(
            attrs={
                'class': 'form-control-c',
                'placeholder':'MM/YY'}))
    cvc = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control-c'}))


class BankTransferForm(forms.Form):
    """
    class for bank transfer form
    """
    iban = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control-c'}))

class WireTransferForm(forms.Form):
    """
    class for wire transfer form
    """
    sending_bank = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control-c'}))
    routing_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control-c'}))
    account_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control-c'}))