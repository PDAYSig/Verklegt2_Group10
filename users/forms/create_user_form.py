from django import forms

from users.models import Profile

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'id', 'password']
        widgets = {
            'user_address': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.TextInput(attrs={'class': 'form-control'}),
        }
