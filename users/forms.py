from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
   
    class Meta:
        model = User
        fields = ['username', 'email', 'password1']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']  

class ProfileUpdateForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES, required=True, label='Gender')
    location = forms.CharField(max_length=30, required=False)
    birthdate = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Profile
        fields = ['image', 'gender', 'location', 'birthdate']
