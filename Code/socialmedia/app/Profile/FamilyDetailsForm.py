from email import message
import email
from enum import unique
from django import forms
from django.core.validators import EmailValidator,MinValueValidator,RegexValidator
import re
from django.forms.widgets import NumberInput  
class FamilyDetailsForm(forms.Form):

    Gender= (
    ('Male','Male'),
    ('Female', 'Female'),
    ('Other','Other'),
    )

    diseases=forms.CharField(required=True,max_length=60,widget=forms.Select(),error_messages={'required':"Please Select Disease"})
    family_person_name=forms.CharField(required=True,max_length=60,error_messages={'required':"Please Provide Member Name"})
    familyemail=forms.EmailField(required=True)