from email import message
from email.policy import default
from logging import PlaceHolder
from django import forms

class EditPostForm(forms.Form):

    post_message=forms.CharField(min_length=3,label='Post Message', widget=forms.TextInput(attrs={'placeholder': 'Write Something Here'}))
    url=forms.CharField(required=False,label='Video url', widget=forms.TextInput(attrs={'placeholder': 'video URL'}))
    imageurls_updated=forms.CharField(min_length=1,label="",widget=forms.TextInput(attrs={'type':'hidden'}))
    uploads=forms.ImageField(required=False,widget=forms.FileInput(attrs={'multiple':True}))
    
