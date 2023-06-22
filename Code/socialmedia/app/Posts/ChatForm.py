from email import message
from email.policy import default
from logging import PlaceHolder
from django import forms

class Chatform(forms.Form):


    chatmessage=forms.CharField(min_length=3,required=True,label='', widget=forms.TextInput(attrs={'placeholder': 'Chat here','id':'chatmessage{{postId}}'}))
    
    
