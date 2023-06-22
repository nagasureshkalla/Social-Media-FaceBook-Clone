
from django.db import models
from app.Models.User import User
from django.utils import timezone
from app.Models.Post import Post

class PostUploadDetails(models.Model):

    postId=models.ForeignKey(Post, on_delete=models.CASCADE)
    uploadId=models.BigAutoField(primary_key=True)
    url = models.ImageField(upload_to='static/postimages',max_length=255,default='')
    createdDate=models.DateTimeField("Post Last created At",default=timezone.now())
    updatedDate=models.DateTimeField("Post Last Updated At",default=timezone.now())