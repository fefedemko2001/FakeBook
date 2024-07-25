from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES, required=True, label='Gender')
    location = forms.CharField(max_length=30, required=False)
    birthdate = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'gender', 'location', 'birthdate']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile = Profile.objects.create(user=user, gender=self.cleaned_data['gender'])
            profile.save()
        return user



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']  


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image',  'gender', 'location', 'birthdate']  
