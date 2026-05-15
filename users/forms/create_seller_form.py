from django import forms

from users.models import Seller

"""
class for a creating a seller form
"""
class CreateSellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        exclude = ['profile', 'id', 'rating']
        widgets = {
            'type': forms.Select(attrs={'class': 'type-select'}),
        }