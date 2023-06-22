from email.utils import formatdate
from traceback import format_list
from django.utils import timezone
from django.db import models
from django.core.validators import EmailValidator,MinValueValidator,RegexValidator
 


# Create your models here.

class User(models.Model):

  reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"

  userId = models.AutoField(primary_key=True)
  email=models.EmailField(max_length = 254,unique=True,default="",validators=[EmailValidator(message="Please enter Valid Email")])
  username=models.CharField(max_length=20,default="",validators=[MinValueValidator(limit_value=6,message="Username must be 6 to 20 characters")])
  password = models.CharField(max_length=255,validators=[RegexValidator(regex=reg,message="Password MustContain 1 Capital, 1 Number, 1 Special character and 8>=length<28")])
  createdDate =  models.DateTimeField("User Created At", default=timezone.now())
  updatedDate = models.DateTimeField("User Last Updated At",default=timezone.now())
  token=models.CharField(max_length=255,default="")
  isVerified=models.BooleanField(default=False)
  lastlogin = models.DateTimeField("User Last LoggedIn At",default=timezone.now())
  isProfileActive=models.BooleanField(default=False)
  photo=models.CharField(max_length=100,default="")