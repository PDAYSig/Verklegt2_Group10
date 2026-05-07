from django.forms import ModelForm
from django import forms
from art.models import art_listing
class ListingCreateForm(ModelForm):
    image = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = art_listing
        exclude = ['id']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'starting_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'artist_name': forms.TextInput(attrs={'class': 'form-control'}),
            'year_created' : forms.DateInput(attrs={'class': 'form-control'}),
            'medium' : forms.Select(attrs={'class': 'form-control'}),
            'style' : forms.Select(attrs={'class': 'form-control'}),
            'mimimum_bid' : forms.NumberInput(attrs={'class': 'form-control'}),
        }