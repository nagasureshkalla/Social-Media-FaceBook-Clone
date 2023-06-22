from django.db import models
from app.Models.User import User
from django.utils import timezone
from datetime import date, datetime
class Likes(models.Model):

    likeId=models.AutoField(primary_key=True)
    postId=models.CharField(max_length=1000,default="",null=False)
    action=models.CharField(max_length=2000,default="")
    authorId=models.CharField(max_length=2000,default="")
    ownerId=models.CharField(max_length=2000,default="")
    createdDate=models.DateTimeField("Like created At",default=timezone.now())
    updatedDate=models.DateTimeField("Like Last Updated At",default=timezone.now())