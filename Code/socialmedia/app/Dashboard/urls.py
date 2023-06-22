from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from app.Dashboard import Dashboard
from app.Posts import post
urlpatterns = [
    path('', Dashboard.index, name='dashboard'),

]