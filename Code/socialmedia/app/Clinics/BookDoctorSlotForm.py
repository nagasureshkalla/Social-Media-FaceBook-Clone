from email import message
import email
from email.policy import default
from django import forms
from django.forms.widgets import NumberInput  



class BookDoctorSlotForm(forms.Form):


    PAYMEMTS= [
    ('Direct consultation', 'Direct consultation'),
    ('Online', 'Online'),
    ]
    
    dateofslot=forms.DateField(widget = NumberInput(attrs={'type':'date'}),error_messages={'required':"Please Provide Date"})
    timeofslot=forms.CharField(max_length=60,widget=forms.Select(),error_messages={'required':"Please Select Time"})
    specialization=forms.CharField(max_length=60,widget=forms.Select(),error_messages={'required':"Please Select Time"})
    coupon=forms.CharField(max_length=60,required=False)
    amount_input=forms.CharField(max_length=60,required=False,widget=forms.TextInput(attrs={'type':'hidden'}))
    payment_mode= forms.CharField(required=True,label='Select your Payment Mode', widget=forms.RadioSelect(choices=PAYMEMTS))
