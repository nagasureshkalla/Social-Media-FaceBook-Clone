
from django.db import models


    
class MedicalHistory(models.Model):
  photo=models.FileField(upload_to='medicaluploads',blank=True)
  userId=models.CharField(max_length=60,default="")

class Interests(models.Model):
  name=models.CharField(max_length=20,default="")
  userId=models.CharField(max_length=60,default="")