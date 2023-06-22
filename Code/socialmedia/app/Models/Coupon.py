from django.db import models
from app.Models.Doctor import Doctor
class Coupon(models.Model):


    couponId=models.AutoField(primary_key=True)
    countofuses=models.IntegerField(max_length=100,default="0")
    couponcode=models.CharField(max_length=100,default="")
    couponamount=models.IntegerField(max_length=100,default="0")