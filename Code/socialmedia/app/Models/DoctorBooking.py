
from django.db import models
from django.utils import timezone
from app.Models.User import User
from app.Models.Doctor import Doctor

class DoctorBooking(models.Model):

    bookinguserId=models.CharField(max_length=100,default="")
    doctorbookingid=models.AutoField(primary_key=True)
    doctorId=models.ForeignKey(Doctor, on_delete=models.CASCADE,default="")
    doctorName=models.CharField(max_length=200,default="")
    specialization= models.CharField(max_length=255)
    rating=models.FloatField(max_length=5,default=0.0)
    slotTime = models.CharField(max_length=100,default="24/7")
    dateofslot=models.DateField()
    messageforanything=models.CharField(max_length=200,default="")
    createdDate=models.DateTimeField("Slot created At",default=timezone.now())
    updatedDate=models.DateTimeField("Slot Last Updated At",default=timezone.now())
    paymentStatus=models.IntegerField(max_length=1,default=0)
    coupunused=models.CharField(max_length=100,default="",blank=True)
    amount=models.IntegerField(default=0)
    paymentmode=models.CharField(max_length=100,default="0")
    appointmentstatus=models.IntegerField(default=0)