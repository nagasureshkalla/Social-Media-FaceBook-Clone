from email import message
from django import forms
from django.core.validators import EmailValidator,MinValueValidator,RegexValidator
class ForgotPasswordForm(forms.Form):

   email=forms.EmailField(max_length = 254,required=True)