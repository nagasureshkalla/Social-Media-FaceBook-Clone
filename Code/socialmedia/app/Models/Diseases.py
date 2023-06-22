from django.db import models

class Diseases(models.Model):
  name = models.CharField(default="",max_length=60,unique=True)