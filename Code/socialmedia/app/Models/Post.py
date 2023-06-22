
from django.db import models
from app.Models.User import User
from django.utils import timezone
from datetime import date, datetime
class Post(models.Model):


    postId=models.CharField(primary_key=True,max_length=100,default="",null=False,unique=True)
    postMessage=models.CharField(max_length=200,default="")
    urlsForUploads = models.CharField(max_length=255)
    likes=models.IntegerField(default=0,max_length=1000000)
    isActive=models.IntegerField(default=0,null=False)
    dislikes=models.IntegerField(max_length=1000000,default=0)
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    authorphoto=models.CharField(max_length=2000,default="")
    createdDate=models.DateTimeField("Post Last created At",default=timezone.now())
    updatedDate=models.DateTimeField("Post Last Updated At",default=timezone.now())
    reasonifrejected=models.CharField(max_length=2000,default="")