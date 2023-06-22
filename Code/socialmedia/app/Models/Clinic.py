
from django.db import models
from app.Models.User import User
from django.utils import timezone
from datetime import date, datetime
class Clinic(models.Model):


    clinicId=models.AutoField(primary_key=True)
    clinicName=models.CharField(max_length=200,default="")
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    specialization= models.CharField(max_length=255)
    rating=models.FloatField(max_length=5,default=0.0)
    availability = models.CharField(max_length=100,default="24/7")
    clinicImage= models.ImageField(upload_to='clinicprofiles',blank=True)
    createdDate=models.DateTimeField("Clinic created At",default=timezone.now())
    updatedDate=models.DateTimeField("Clinic Last Updated At",default=timezone.now())
    