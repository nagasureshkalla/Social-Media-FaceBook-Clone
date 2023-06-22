from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path

from app.MyPosts import Myposts

urlpatterns = [
    path('', Myposts.index, name='myposts'),

    path('editpost/<postId>',Myposts.editPost,name='editpost'),

    path('searchmyposts/',Myposts.search_mypost,name='searchmyposts'),
    path('getsearchedmyposts/',Myposts.get_search_post,name='getsearchedmyposts')
  

]