
from django.db import models
from app.Models.User import User
from django.utils import timezone
from datetime import date, datetime
class Messages(models.Model):

    messageId=models.AutoField(primary_key=True)
    postId=models.CharField(max_length=100,default="",null=False)
    chatMessage=models.CharField(max_length=2000,default="")
    authorphotourl = models.CharField(max_length=255,default="")
    authorname = models.CharField(max_length=255,default="")
    authorId=models.CharField(max_length=1000,default="")
    createdDate=models.DateTimeField("Chat Last created At",default=timezone.now())
    updatedDate=models.DateTimeField("Chat Last updated At",default=timezone.now())