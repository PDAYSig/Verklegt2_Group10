from django.forms import ModelForm
from django import forms
from art.models import art_listing
class ListingCreateForm(ModelForm):
    class Meta:
        model = art_listing
        exclude = ['id', 'seller']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'starting_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'artist_name': forms.TextInput(attrs={'class': 'form-control'}),
            'year_created' : forms.DateInput(attrs={'class': 'form-control'}),
            'medium' : forms.Select(attrs={ 'class': 'form-control'}),
            'dimension': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '?x?'}),
            'style' : forms.Select(attrs={'class': 'form-control'}),
            'minimum_bid' : forms.NumberInput(attrs={'class': 'form-control'}),
            'provenance' : forms.Textarea(attrs={'class': 'form-control'}),
        }