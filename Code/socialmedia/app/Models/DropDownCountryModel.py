from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class State(models.Model):
    country = models.CharField(max_length=40)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=124)
    state = models.CharField(max_length=40,default="")

    def __str__(self):
        return self.name