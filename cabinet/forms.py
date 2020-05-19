from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class RegForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='')
	username = forms.CharField(max_length = 100, help_text='')
	password1 = forms.CharField(max_length = 100, help_text='')
	password2 = forms.CharField(max_length = 100, help_text='')

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2', ]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=25)
    password = forms.CharField(max_length=100)