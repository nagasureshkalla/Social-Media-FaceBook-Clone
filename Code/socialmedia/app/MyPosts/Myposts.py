
from datetime import datetime,date
from json import JSONDecodeError
import json
import os
import random
import threading
from urllib import request
from app.Models.Diseases import Diseases
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_protect 
from django.http import HttpResponse, JsonResponse
from app.MessageHandler import SOMETHING_HAPPENED
from app.Posts.PostForm import PostForm
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from app.Models.Post import Post
from app.Models.PostUploadDetails import PostUploadDetails
from app.Models.User import User
from app.Models.Followers import Followers
from app.Models.Messages import Messages
from app.Posts.ChatForm import Chatform
from app.Models.Followers import Contributers
from app.Models.DropDownCountryModel import State,Country,City
from app.Models.Clinic import Clinic
from app.Models.UserDetails import UserDetails
from app.Models.Doctor import Doctor
from app.MyPosts.EditPostForm import EditPostForm

@csrf_protect
def index(request):  # Main page of Myposts

    # user=UserDetails.objects.filter(userId=request.session['userId'])
    if not request.session.has_key('userId') or request.session['userId']=='':
        return redirect("/")
    else:
        if request.method=='GET':

            print("\n\nAT index\n\n")
            posts=Post.objects.filter(author=request.session['userId'])  # List of my posts
            list_of_objects=[]
            for i in posts:
                object=DummyPost(i.postId,i.postMessage,i.urlsForUploads,i.author,i.likes,i.dislikes,i.updatedDate,i.authorphoto,i.isActive,i.reasonifrejected)
                object.getAllUrls()
                list_of_objects.append(object)

            template = loader.get_template('myposts.html')
            context = {
                'posts':list_of_objects,
                }
            return HttpResponse(template.render(context, request))
        
                
                


# This is Edit Post Page redirection where we can edit the Post
def editPost(request,postId):
    if not request.session.has_key('userId') or request.session['userId']=='':
        return redirect("/")
    else:
        if request.method=='GET':
            print("\n\nAT Edit Post Page")

            post=Post.objects.get(postId=postId)
            editform=EditPostForm()

            ########  Setting the Initial Values ############
            editform.fields["post_message"].initial=post.postMessage
            if post.urlsForUploads !="":
                editform.fields["imageurls_updated"].initial=post.urlsForUploads
            else:
                editform.fields["imageurls_updated"].initial=","
            ########  Setting the Initial Values ############

            template = loader.get_template('editpost.html')
            context = { 
            'editpost':editform,
            'urls':post.urlsForUploads,
            'postId':postId

            }
            return HttpResponse(template.render(context, request))
        elif request.method=='POST' and 'submiteditpostdetails' in request.POST: # if Edit and submit the details 
            print("\n\nPOST method in EditPost page\n\n")

            submitEditedPostDetails(request,postId)

            return redirect('/myposts')

            


# Submit the Edited details and update the DB 
def submitEditedPostDetails(request,postId):
    print("In submitEditedPostDetails function")
    if not request.session.has_key('userId') or request.session['userId']=='':
        return redirect("/")
    else:
     
        editform = EditPostForm(request.POST)

        

        if editform.is_valid():
            print("\n\nEdited Post form details are valid\n\n")
            postMessage=editform.cleaned_data.get('post_message')
            url=editform.cleaned_data.get('url')
            imageurls=request.POST.get('imageurls_updated') 
            print("\n\n",postMessage,"\n",url)
            print("\n\IMAGE URLS : :::",imageurls,"\n\n")
            try:
                files=request.FILES.getlist('uploads')
                print("FILES PROFILE",files)
            except:
                files=[]

            

            try:
                
                post=Post.objects.get(postId=postId)
                # post=Post(postId=postId,postMessage=postMessage,urlsForUploads="",isActive=True,author=user,likes=0,dislikes=0,createdDate=timezone.now(),updatedDate=timezone.now())
                # post.save()

                urls_all=upload_files(request,files,imageurls,url,post) #  upload all new images

                print("ALL URLS",urls_all)

                post.postMessage=postMessage
                post.isActive=0  # UnderReview
                post.urlsForUploads=urls_all
                post.updatedDate=timezone.now()
                post.save()  # update the Post table with urls

                
                
            except:
                messages.add_message(request, messages.ERROR, SOMETHING_HAPPENED)
        else:
            print("\n\nEdited Details are not valid")
        

# upload the newly added files to DB
def upload_files(request,files,updatedurls,videourl,postid):
    urls=""
    try:
         for i in files:
            PostUploadDetails(postId=postid,url=i).save()
            urls=urls+",/postimages/"+str(i)
    except:
        messages.add_message(request, messages.ERROR, SOMETHING_HAPPENED+" At urls")

    updatedlist=list(filter(None, updatedurls.split(",")))  # if the old images are deleted , remove from the list
    for i in updatedlist:
        urls=urls+","+i

    print("\n\nUPDATED URLS",updatedlist)

    return urls

# Model class for Post object align clearly
class DummyPost:

    def __init__(self,postid,memmage,urls,author,likes,dislikes,date,authorphoto,isActive,reason):
        self.postId=postid
        self.message=memmage
        self.likes=likes
        self.dislikes=dislikes
        self.author=author
        self.posturls=urls
        self.date=date
        self.postage=""
        self.authorphoto=authorphoto
        self.isActive=isActive
        self.reason=reason
       

    # get all image urls in a list
    def getAllUrls(self):
        print("At getAllUrls page")
        
        urls=self.posturls
        urls=urls.split(',')
        del urls[0]
        self.posturls=urls


# This is a Search Functionality for the MyPosts
def search_mypost(request):
    postname=request.GET.get('postmessage')
    payload=[]
    
    if postname:
        postobjects=Post.objects.filter(postMessage__icontains=postname,author=request.session['userId'])
        
        for i in postobjects:
            payload.append(i.postMessage)
           
    print("Searched Data: ",payload)
    return JsonResponse({'status':200,'data':payload})

# when clicked on the post searched , will return the Post object ID and redirect to edit page
def get_search_post(request):
    postname=request.GET.get('postmessage')
    
    
    print("POST NAME",postname)
    postobjects=Post.objects.get(postMessage=postname)
    print(postobjects)
    return JsonResponse({'status':200,'data':postobjects.postId})
    