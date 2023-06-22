
from datetime import datetime,date
from json import JSONDecodeError
import json
import os
import random
import threading
from urllib import request
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
# Create your views here.

@csrf_protect
def index(request):  # Main page for Posts/Newsfeed Page

    
    if not request.session.has_key('userId') or request.session['userId']=='':
        return redirect("/")
    else:
        if request.session['userId']=='':
            return redirect('/')
        user=User.objects.get(userId=request.session['userId'])  # get the User the Object
        print(user.photo)

        
                
        if  'post' in request.POST and request.method=='POST':   # Submi the Post , Messages and Images
            checkforactivesession(request)
            postform = PostForm(request.POST)

            if postform.is_valid():
                print("\n\nPost form details are valid\n\n")

                
                postMessage=postform.cleaned_data.get('post_message') # get the Post Message
                url=postform.cleaned_data.get('url')  # get the Post Uploads urls
                print("\n\n",postMessage,"\n",url)
                try:
                    files=request.FILES.getlist('uploads')  # get the Files
                    print("FILES PROFILE",files)
                except:
                    files=[]

                postId=str(request.session['userId'])+str(date.today())+str(random.randint(1,100000))  # create a unique PostId

                try:
                    post=Post(postId=postId,postMessage=postMessage,authorphoto=str(user.photo),urlsForUploads="",isActive=True,author=user,likes=0,dislikes=0,createdDate=timezone.now(),updatedDate=timezone.now())
                    post.save()  # save the Post with blank Image urls and get the Post ID 

                    urls_all=upload_files(request,files,url,post) #  upload all images and get all urls as string

                    print("ALL URLS",urls_all)

                    post.urlsForUploads=urls_all
                    post.save()  # update the Post table with urls
                except:
                    messages.add_message(request, messages.ERROR, SOMETHING_HAPPENED)
        
        else:
            checkforactivesession(request) # check if user is loggedin
            try:
                postform=PostForm()
                chatform=Chatform()

                follow=[]
                follower=Followers.objects.filter(userId=request.session['userId']) # get the followers 
                for i in follower:
                    follow.append(i.followerId)

                contrib=[]
                contributers=Contributers.objects.filter(userId=request.session['userId']) # get the Contributers 
                for i in contributers:
                    contrib.append(i.contributerId)

                following=[]
                followe=Followers.objects.filter(followerId=request.session['userId']) # get the following 
                for i in followe:
                    following.append(i.userId)


                follow_contrib=follow+contrib+following
                follow_contrib=list(set(follow_contrib))   # remove the Duplicates
                print(follow)

                # Set the isActive=1 , when going to Production/Testing to below query
                postdetails=Post.objects.filter(author__in=follow_contrib)  # get the Posts of Followers, contributers, Following 
                
                print(postdetails)

                allpostobjects=[]
                for i in postdetails:
                    postobject=PostDetails(i.postId,i.postMessage,i.urlsForUploads,i.author.username,i.author.userId,i.likes,i.dislikes,i.updatedDate,i.authorphoto)
                    postobject.getAllUrls()
                    postobject.calpostage()
                    allpostobjects.append(postobject)
                    
                print(len(allpostobjects))
            
            
            except:
                messages.add_message(request, messages.ERROR, SOMETHING_HAPPENED)

            template = loader.get_template('post.html')
            context = {
                'data':request.session['username']+" LoggedIN",
                'form':postform,
                'postdata':allpostobjects,
                'usersphoto':user,
                'chatform':chatform,
                'followers':User.objects.filter(userId__in=follow),
                'contributers': User.objects.filter(userId__in=contrib),
                'following':User.objects.filter(userId__in=following),
                'domain':get_current_site(request),
                'searchdata':{}
                }
            return HttpResponse(template.render(context, request))
        checkforactivesession(request)
        return HttpResponseRedirect("/post")


# when user clicks on any post it wil redirect to new page with all details of post
def redirecttopostdetails(request,postId):
    # postobject=[]
    chatform=Chatform()
    i=Post.objects.get(postId=postId)

    postobject=PostDetails(i.postId,i.postMessage,i.urlsForUploads,i.author.username,i.author.userId,i.likes,i.dislikes,i.updatedDate,i.authorphoto)
    postobject.getAllUrls()
    postobject.calpostage()
    
    # postobject.append(postobject)

    template = loader.get_template('postdetails.html')
    context = {
        'i':postobject,
        'domain':get_current_site(request),
        'chatform':chatform,
        }
    return HttpResponse(template.render(context, request))
  

# upload the post images to DB
def upload_files(request,files,url,postid):
    urls=""
    try:
        for i in files:
            PostUploadDetails(postId=postid,url=i).save()
            urls=urls+",/postimages/"+str(i)
    except:
        messages.add_message(request, messages.ERROR, SOMETHING_HAPPENED+" At urls")

    if not url=="" or not url=='':
        PostUploadDetails(postId=postid,url=url).save()
        urls=urls+","+str(url)
    return urls


# Models class for Handling/ align the Post object cleanly
class PostDetails:

    def __init__(self,postid,memmage,urls,author,authorId,likes,dislikes,date,authorphoto):
        self.postId=postid
        self.message=memmage
        self.likes=likes
        self.dislikes=dislikes
        self.author=author
        self.posturls=urls
        self.date=date
        self.postage=""
        self.authorphoto=authorphoto
        self.authorId=authorId

    # get the urls as list
    def getAllUrls(self):
        print("At getAllUrls page")
        
        urls=self.posturls
        urls=urls.split(',')
        print(urls)
        del urls[0]
        print(urls)
        self.posturls=urls
    # calculate Post age
    def calpostage(self):
        print("At cal Age of post",self.date)
        b = timezone.now()
        print("now datetime,",b)
        a = self.date
        
        c = a-b
        
        print('Difference: ', c)
        if "days" in str(c) :
            self.postage=str(c).split(",")[0] +" Ago"
        elif "-1" in str(c):
            minutes = c.total_seconds() / 60
            if str(minutes).split('.')[1]=="0":
                self.postage="Just Now"
            else:
                if len(str(minutes).split('.')[0])>2:
                    
                    self.postage=str(int(str(minutes).split('.')[0])//60 )+" Hours Ago"
                elif str(minutes).split('.')[0]=="0" or str(minutes).split('.')[0]=='0':
                    self.postage="Just Now"
                else:
                    self.postage=str(minutes).split('.')[0]+" Minutes Ago"
        self.postage=self.postage[1:]
        print(self.postage)


# Thread Used for posting the details ( Never used , might use in future )
class PostThread(threading.Thread):
    def __init__(self,postform,request,user):
        self.postform=postform
        self.user=user
        self.request=request
        threading.Thread.__init__(self)
    def run(self):
        pass

       
# check if the user is loggedIN
def checkforactivesession(request):
    if not request.session.has_key('userId') or request.session['userId']=='':
        return redirect("/")
#

# Search Functionality of Post Page, Search all post in DB and return the post messages
def search_post(request):

    postname=request.GET.get('postname')
    payload=[]
    searchpostIds=[]
    allpostobjects=[]
    if postname:
        postobjects=Post.objects.filter(postMessage__icontains=postname)
        for i in postobjects:
            payload.append(i.postMessage)
            searchpostIds.append(i.postId)



    print("SEARCHED Data",allpostobjects)
    return JsonResponse({'status':200,'data':payload})

# when user clicked on the searched post, will redirctto post details page
def get_search_post(request):
    postname=request.GET.get('postname')
    if postname:
        postobjects=Post.objects.get(postMessage__icontains=postname)
        return JsonResponse({'status':200,'data':postobjects.postId})
    