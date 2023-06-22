from email import message
import email
from email.policy import default
from django import forms
from django.core.validators import EmailValidator,MinValueValidator,RegexValidator
import re
from django.forms.widgets import NumberInput  



class UserDetailsForm(forms.Form):



    Gender= (
    ('Male','Male'),
    ('Female', 'Female'),
    ('Other','Other'),
    )
    firstname=forms.CharField(max_length=60,error_messages={'required':"Please Provide Firstname"})
    lastname=forms.CharField(max_length=60,error_messages={'required':"Please Provide Lastname"})
    dob=forms.DateField(widget = NumberInput(attrs={'type':'date'}),error_messages={'required':"Please Provide Date of Birth"})
    gender=forms.CharField(max_length=6,widget=forms.Select(choices=Gender),error_messages={'required':"Please Provide Gender"})
    email=forms.EmailField(disabled=True,required=False)
    mobile= forms.CharField(widget=forms.TextInput(attrs={'type': 'tel', 'placeholder':"123-45-678",'pattern':"[0-9]{6,15}"}),validators = [RegexValidator(regex = r"^\+?1?\d{8,15}$")],error_messages={'required':"Enter a Valid Mobile Number"})
    photo=forms.ImageField(required=False,widget=forms.FileInput(attrs={'onclick':'previewFile()','onchange':'previewFile()'}))
    country=forms.CharField(max_length=60,widget=forms.Select(),error_messages={'required':"Please Select Country"})
    state=forms.CharField(max_length=60,widget=forms.Select(),error_messages={'required':"Please Select State"})
    city=forms.CharField(max_length=60,widget=forms.Select(),error_messages={'required':"Please Select State"})
    union_council=forms.CharField(max_length=10,error_messages={'required':"Please Provide Union Council"})
    address=forms.CharField(max_length=60,widget=forms.Textarea,error_messages={'required':"Please Provide Address"})
    postal_code=forms.CharField(required=True,max_length=10,error_messages={'required':"Please enter Postal Code"})
    smoking= forms.CharField(required=True,label='Do you Smoke?', widget=forms.RadioSelect(choices=[('yes','Yes'),('no','No')]),error_messages={'required':"Please select an option"})
    alchol= forms.CharField(required=True,label='Do you Drink Alcohol?', widget=forms.RadioSelect(choices=[('yes','Yes'),('no','No')]),error_messages={'required':"Please select an option"})
    previous_existing_history_diabets =forms.BooleanField(required=False)
    Hipertension =forms.BooleanField(required=False)
    Arthritis =forms.BooleanField(required=False)
    Allergies =forms.BooleanField(required=False)
    Previous_Surgery =forms.BooleanField(required=False)
    Any_Medication =forms.BooleanField(required=False)
    BloodPressure =forms.BooleanField(required=False)
    Temparature =forms.BooleanField(required=False)
    HeratRate =forms.BooleanField(required=False)
    RespiratoryRate=forms.BooleanField(required=False)
    Weight =forms.BooleanField(required=False)
    Height =forms.BooleanField(required=False)
    images=forms.FileField(required=False,widget=forms.FileInput(attrs={'multiple':True}))

    


    