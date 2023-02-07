from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  


class SignupForm(UserCreationForm):
	email = forms.EmailField(label='email')