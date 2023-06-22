
from datetime import datetime
from multiprocessing import context
import os
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect 
from app.MessageHandler import SOMETHING_HAPPENED
from app.Posts.PostForm import PostForm
from django.http import HttpResponseRedirect
from app.Models.Post import Post
from app.Models.PostUploadDetails import PostUploadDetails
from app.Models.User import User
from app.Models.Followers import Followers
from app.Posts.ChatForm import Chatform
from app.Models.Messages import Messages
from app.Models.Likes import Likes
from app.Models.Followers import Contributers
# Create your views here.

@csrf_protect
def index(request):     # Main function for chat Functionality

    if request.session['userId']=='':
            return redirect('/')

    if  'postchatmessage' in request.POST and request.method=='POST':
        chatform = Chatform(request.POST)
    
        if chatform.is_valid():  # Never used 
            print("Chat message details are valid")
            postId=chatform.cleaned_data.get('postId')
            print("\n\n\n",postId,"\n\n\n\n")
            pass
            
    message=[]
    try:
        chatform=Chatform()
        # chatform.chatmessage.widget_attrs
        
    except:
        messages.add_message(request, messages.ERROR, SOMETHING_HAPPENED)

    template = loader.get_template('chat.html')
    context = {
        'messages':message,
        'chatform':chatform
        }


    return HttpResponse(template.render(context, request))
   
# Get all the Messages for the Post Id
def getMessages(request, postId):
    if request.session['userId']=='':
            return redirect('/')
    print('At Get Chat Messages Function for PostId :',postId)
    # get the messages for postId orderby upadatedDate
    message=Messages.objects.filter(postId=postId).order_by('updatedDate')
    
    print('\n\n',list(message.values()),'\n\n')
    context = {
            'messages':list(message.values()),
            'likedislikes':getLikes(postId)
            
            }
    
    return JsonResponse(context)

# Submit  the Likes/Dislikes on the Post
def postLikes(request,postId,author,action):
    if request.session['userId']=='':
            return redirect('/')
    print("Likes Successfully : ",action)
    # likes=Likes.objects.filter("SELECT * FROM app_likes WHERE postId  = '%s' AND authorId = '%s' " %(postId, request.session['userId']))
    likes=Likes.objects.filter(postId=postId, authorId=request.session['userId'])

    print("\n\nPOSTLIKES  AuthorID:",author," Action:",action,"postId:",postId," Session:",request.session['userId'])
    try:
        conrtib=Contributers.objects.filter(userId=author,contributerId=request.session['userId']).first()
        # check if contributing for the post for the first time
        if int(action) and conrtib is None:

            print("\n\nContributes adding")
            # user adding to the contributers table for the post
            Contributers(userId=author,postId=postId,contributerId=request.session['userId'],contributerName=request.session['username'],createdDate=timezone.now(),updatedDate=timezone.now()).save()
            print("\n\nContributes Added")
        
    except:
        print("\n\nContributes NOT added")
       
        

    if likes : # if liking/Disliking which is already liked/disliked
        for i in likes:
            i.action=action
            i.updatedDate=timezone.now()
            i.save()
            print("Updated old Like")
        
    else: #  Dislike/liking the Post for the firsttime the Post
        likes=Likes(postId=postId,action=action,authorId=request.session['userId'],ownerId=author,createdDate=timezone.now(),updatedDate=timezone.now())
        likes.save()
        print("Saved new Like")
    
    
    return JsonResponse({})
    
# get the likes/ dislikes  for the post
def getLikes(postId):
   
    like=0
    dislike=0
    likes=Likes.objects.filter(postId=postId)
    # print(likes.action)
    for i in likes:
        if i.action == '1':
            like=like+1
        else:
            dislike=dislike+1
    context={
        'likes':like,
        'dislikes':dislike
    }
    print(context)
    return context


# function handles the Message posted by user and update in DB
@csrf_protect
def postchatmessage(request,postId):
    
    if request.session['userId']=='':
            return redirect('/')
    print("At postchatmessage function")
    if request.method=='POST' : # Submit the chat message
        chatform = Chatform(request.POST)
        print("At postchatmessage validation ")
        
        print("Chat message details are valid")
        message_user= request.POST['message']
        postId= postId 
        print("\n\n\n",message_user,"\n\n",postId,"\n\n\n\n")
        postMessageToPostChat(request,message_user,postId)


    # GEt the Chat Messages
    message=[]
    try:
        chatform=Chatform()
        
    except:
        messages.add_message(request, messages.ERROR, SOMETHING_HAPPENED)

    template = loader.get_template('chat.html')
    context = {
        'messages':message,
        'chatform':chatform
        }
    # return JsonResponse(context)

    return HttpResponse(template.render(context, request))



# post the chat message to Messages table
def postMessageToPostChat(request,message,postId):
    try:
        message=Messages(postId=postId,chatMessage=message,authorphotourl=request.session['photo'],authorname=request.session['username'],authorId=request.session['userId'],createdDate=timezone.now(),updatedDate=timezone.now())
        message.save()
    except:
        messages.add_message(request, messages.ERROR, SOMETHING_HAPPENED)


# check for user loggedIn
def checkforactivesession(request):
    if request.session['userId']=='':
            return redirect('/')