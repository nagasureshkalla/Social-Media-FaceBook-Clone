from email import message
from django import forms
from django.core.validators import EmailValidator,MinValueValidator,RegexValidator
class ResetPasswordForm(forms.Form):
    password = forms.CharField(required=True,widget=forms.PasswordInput)
    repassword = forms.CharField(required=True,widget=forms.PasswordInput)
