
from email.utils import formatdate
from traceback import format_list
from django.utils import timezone
from django.db import models
from django.core.validators import EmailValidator,MinValueValidator,RegexValidator
from app.Models.User import User


class UserDetails(models.Model):
  firstname=models.CharField(max_length=60)
  lastname=models.CharField(max_length=60)
  dob=models.CharField(max_length=10)
  gender=models.CharField(max_length=6)
  mobile=  models.CharField(validators = [RegexValidator(regex = r"^\+?1?\d{8,15}$")], max_length = 16, unique = True)
  userId=models.ForeignKey(User, on_delete=models.CASCADE)
  email=models.EmailField(max_length = 254,unique=True,default="",validators=[EmailValidator(message="Please enter Valid Email")])
  photo=models.ImageField(upload_to='usersprofiles',blank=True)
  country=models.CharField(max_length=60,default="")
  state=models.CharField(max_length=60,default="")
  city=models.CharField(max_length=60,default="")
  union_council=models.CharField(max_length=10,default="")
  address=models.CharField(max_length=60,default="")
  postal_code=models.CharField(max_length=10,default="")
  smoking= models.CharField(max_length=10,default="")
  alchol= models.CharField(max_length=10,default="")
  previous_existing_history_diabets =models.BooleanField(default=0)
  Hipertension =models.BooleanField(default=0)
  Arthritis =models.BooleanField(default=0)
  Allergies =models.BooleanField(default=0)
  Previous_Surgery =models.BooleanField(default=0)
  Any_Medication =models.BooleanField(default=0)
  BloodPressure =models.BooleanField(default=0)
  Temparature =models.BooleanField(default=0)
  HeratRate =models.BooleanField(default=0)
  RespiratoryRate=models.BooleanField(default=0)
  Weight =models.BooleanField(default=0)
  Height =models.BooleanField(default=0)
  interests=models.TextField(max_length=1000,default="")