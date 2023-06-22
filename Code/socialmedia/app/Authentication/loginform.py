from email import message
from django import forms
from django.core.validators import EmailValidator,MinValueValidator,RegexValidator
class UserLoginForm(forms.Form):

    email=forms.EmailField(max_length = 254,required=True)
    password = forms.CharField(required=True,widget=forms.PasswordInput)
