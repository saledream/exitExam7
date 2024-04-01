from typing import Any
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from EECommittee.models import Department 
from django.conf import settings 
from django import forms 
from .models import User 
from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Layout, Submit 
from django.contrib.auth.forms import AuthenticationForm 
from django.forms import ModelForm 

class SignUpForm(UserCreationForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all()) 
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None
   
    class Meta:
        model = User
        fields = ["email",'username','password1','password2',"department"]
        

class LoginForm(forms.Form):
     email = forms.EmailField() 
     password = forms.CharField(widget=forms.PasswordInput) 

     