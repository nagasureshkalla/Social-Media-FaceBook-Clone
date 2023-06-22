from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from app.Posts import post
from app.Posts import ChatHistory
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', post.index, name='post'),
    path('getchatmessages/<postId>',ChatHistory.getMessages,name='chatmessages'),
    path('',ChatHistory.index,name='postchatmessage'),
    path('postlikes/<postId>/<author>/<action>',ChatHistory.postLikes,name='postlike'),
    path('postchatmessage/<postId>',ChatHistory.postchatmessage,name='postchatmessages'),
    path('postdetails/<postId>',post.redirecttopostdetails,name='postdetailview'),
    path('searchposts/',post.search_post,name='searchpost'),
    path('getsearchedpostid/',post.get_search_post,name='getsearchpost')
    
]+static(settings.MEDIA_URL,Document_riit=settings.MEDIA_ROOT)