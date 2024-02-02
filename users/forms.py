from django import forms
from.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class Createuserform(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email
    

class Updateuserform(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists:
            raise ValidationError('Email exists')
        return self.cleaned_data    


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = []