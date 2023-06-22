from email import message
from email.policy import default
from logging import PlaceHolder
from django import forms

class PostForm(forms.Form):

    post_message=forms.CharField(label='Post Message', widget=forms.TextInput(attrs={'placeholder': 'Write Something Here'}))
    uploads=forms.ImageField(required=False,widget=forms.FileInput(attrs={'multiple':True}))
    url=forms.CharField(required=False,label='Video url', widget=forms.TextInput(attrs={'placeholder': 'video URL'}))
    
