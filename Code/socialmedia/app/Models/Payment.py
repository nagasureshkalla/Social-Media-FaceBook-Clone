
from django.db import models
from app.Models.User import User
from django.utils import timezone

class Payment(models.Model):

    paymentorderId=models.CharField(max_length=100,default="",null=False,primary_key=True,unique=True)
    amount=models.IntegerField(max_length=100,default=0)
    doctorbookingid=models.CharField(max_length=1000,default="")
    doctorId=models.CharField(max_length=1000,default="")
    userId=models.CharField(max_length=1000,default="")
    createdDate=models.DateTimeField("Payment Last created At",default=timezone.now())
    updatedDate=models.DateTimeField("Payment Last updated At",default=timezone.now())
    refundStatus=models.BooleanField("Refund Status",default=0)