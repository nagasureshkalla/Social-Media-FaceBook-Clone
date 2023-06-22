
from django.utils import timezone
from django.db import models
from app.Models.User import User
from app.Models.Post import Post



class Followers(models.Model):
  userId=models.CharField(default="",max_length=1000)
  followerId = models.CharField(default="",max_length=1000)  # the one who is following the userId
  followerName = models.CharField(default="",max_length=1000) 
  createdDate=models.DateTimeField("Follower created At",default=timezone.now())
  updatedDate=models.DateTimeField("Follower Last Updated At",default=timezone.now())

class Contributers(models.Model):
  userId=models.CharField(default="",max_length=1000)
  postId=models.CharField(default="",max_length=1000)
  contributerId=models.CharField(default="",max_length=1000)
  contributerName=models.CharField(default="",max_length=1000)
  createdDate=models.DateTimeField("Contributer created At",default=timezone.now())
  updatedDate=models.DateTimeField("Contributer Last Updated At",default=timezone.now())