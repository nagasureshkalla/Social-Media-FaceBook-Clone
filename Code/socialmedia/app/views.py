
import os
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from app.Models.User import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect 
# Create your views here.

@csrf_protect
def index(request):
    if request.method=='POST':
        img=request.FILES['profile']
        addUser(img)
        messages.add_message(request, messages.SUCCESS, "Add user.....")
    
    user=getRecordofUser()

    mymembers = User.objects.all().values()
    output = ""
    for x in mymembers:
        output += x["username"]
    
    
    # variables = RequestContext(request,{
    # 'carx':user.photo.url})

    template = loader.get_template('home.html')
    context = {
    'mymembers': mymembers,
    'image':user.photo.url
    }
    return HttpResponse(template.render(context, request))




def addUser(img):
    member = User(username="Naga", password="Suersh",isProfileActive=True,photo=img)
    member.save()
    
def getRecordofUser():
    try:
        user=User.objects.get(userId=67)
        print("\n\n\n",user.photo)  
        return user
    except :
        print("Exception")
        return User(username="Naga", password="Suersh",isProfileActive=True,photo="usersprofiles/images_35UBCfj.jpeg")
    
    
def delallusers():
    member = User.objects.all()
    member.delete()