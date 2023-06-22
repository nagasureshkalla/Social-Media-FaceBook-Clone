
from django import forms
from django.db import models



class InterestNames(models.Model):
  name=models.CharField(max_length=20,default="")

class InterestNamesForm(forms.Form):
  interestname=forms.CharField(min_length=3,max_length=20)