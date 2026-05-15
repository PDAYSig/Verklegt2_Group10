from django.forms import ModelForm
from django import forms
from art.models import art_listing
class ListingCreateForm(ModelForm):
    date_added = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%y-%m-%d'])

    """
    class for listing forms that with everything you can give a value in the form
    """
    class Meta:
        model = art_listing
        exclude = ['id', 'seller', 'date_added', 'current_bid']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'starting_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'artist_name': forms.TextInput(attrs={'class': 'form-control'}),
            'year_created' : forms.DateInput(attrs={'type': 'date'}),
            'Edition' : forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False),
            'medium' : forms.Select(attrs={ 'class': 'form-control'}),
            'dimension': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '?x?'}),
            'style' : forms.Select(attrs={'class': 'form-control'}),
            'provenance' : forms.Textarea(attrs={'class': 'form-control'}),
        }
