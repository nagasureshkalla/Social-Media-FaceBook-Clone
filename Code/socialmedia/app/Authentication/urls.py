from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path

from app.Authentication import Auth
urlpatterns = [
    path('', Auth.index, name='signup'),
    path('accountactivate/<uid64>/<token>',Auth.activate_account,name="accountactivate"),
    path('resetpassword/<uid64>/<token>',Auth.reset_password,name="passwordreset"),
    path('logout',Auth.logout,name="logout")
]