from django.db import models
from django.utils import timezone

from app.Models.Clinic import Clinic
from app.Models.User import User
class Doctor(models.Model):

    userId=models.CharField(max_length=100,default="0")
    doctorId=models.AutoField(primary_key=True)
    clinicId=models.ForeignKey(Clinic, on_delete=models.CASCADE,default="")
    doctorName=models.CharField(max_length=100,default="0")
    country=models.CharField(max_length=100,default="")
    state=models.CharField(max_length=100,default="")

    city=models.CharField(max_length=100,default="")
    specialization=models.CharField(max_length=100,default="")
    availabilityFrom=models.CharField(max_length=100,default="")
    availabilityTo=models.CharField(max_length=100,default="")
    doctorImage= models.ImageField(upload_to='clinicprofiles',blank=True)

    createdDate=models.DateTimeField("Clinic created At",default=timezone.now())
    updatedDate=models.DateTimeField("Clinic Last Updated At",default=timezone.now())
    experience=models.FloatField(max_length=100,default=0.0)
    rating=models.FloatField(max_length=10,default=0.0)