from django import forms

from users.models import Profile

"""
class for creating a profile form
"""
class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'id', 'password', 'is_seller']
        widgets = {
            'user_address': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.TextInput(attrs={'class': 'form-control'}),
        }
