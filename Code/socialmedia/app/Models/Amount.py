
from django.db import models
from app.Models.Doctor import Doctor
class Amount(models.Model):


    amountId=models.AutoField(primary_key=True)
    doctorId=models.ForeignKey(Doctor, on_delete=models.CASCADE,default="")
    specilization=models.CharField(max_length=200,default="")
    amount=models.IntegerField(default=0)