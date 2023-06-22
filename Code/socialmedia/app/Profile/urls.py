from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from app.Profile import UserDetails

urlpatterns = [
    path('userdetails/', UserDetails.index, name='userdetails'),

    path('insertinterest/<str:interest>', UserDetails.interests, name='interests')

   
]

