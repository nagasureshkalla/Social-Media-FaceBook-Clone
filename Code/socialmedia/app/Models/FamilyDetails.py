
from django.db import models
from app.Models.User import User

class FamilyDetails(models.Model):

    diseases=models.CharField(max_length=60,error_messages={'required':"Please Select Disease"})
    family_person_name=models.CharField(max_length=60,error_messages={'required':"Please Provide Member Name"})
    familyemail=models.EmailField()
    userId=models.ForeignKey(User, on_delete=models.CASCADE)