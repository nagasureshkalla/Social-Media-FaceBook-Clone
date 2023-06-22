
from django import forms



class DocumentForm(forms.Form):

  documents=forms.FileField(required=False,widget=forms.FileInput(attrs={'multiple':True}))
  