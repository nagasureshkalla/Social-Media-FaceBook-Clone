from audioop import reverse
from base64 import urlsafe_b64decode, urlsafe_b64encode
import datetime
import imp
import random
import json,os
import time
# python standard lib
import base64, secrets, io

# django and pillow lib
from PIL import Image
from django.core.files.base import ContentFile
from turtle import hideturtle
from urllib.request import urlopen
from django.contrib.auth.hashers import make_password,check_password
from readline import get_current_history_length
import string
from django.utils import timezone
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
import threading
from django.contrib import messages
from django.template import loader
from django.utils.html import format_html
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm
from django.shortcuts import redirect, render
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_protect
from app.Models.User import User
from app.Models.UserDetails import UserDetails
from app.Models.FamilyDetails import FamilyDetails
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from app.MessageHandler import SOMETHING_HAPPENED,ACCOUNT_ALREADY_EXISTS,ACCOUNT_ADDED,DEFAULT_IMAGE,BLANK
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from base64 import urlsafe_b64encode,urlsafe_b64decode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage
from django.conf import settings
from app.Authentication.signupform import UserForm
from app.Authentication.loginform import UserLoginForm
from app.Authentication.forgotpasswordform import ForgotPasswordForm
from app.Authentication.resetpasswordform import ResetPasswordForm
from app.Profile.UserDetailsForm import UserDetailsForm
from app.Models.DropDownCountryModel import State,Country,City
from app.Profile.FamilyDetailsForm import FamilyDetailsForm
from app.Models.Diseases import Diseases
from app.Models.MedicalHistory import MedicalHistory,Interests
from app.Models.InterestNames import InterestNames
from app.Models.InterestNames import InterestNamesForm

#  Userdetail spage will appear when user login for the first time

@csrf_protect
def index(request):   # Main function for the User details Page

    familymemberslist=[]
    try:
        userobject=User.objects.get(userId=request.session['userId']) # get the User details
    except:
        userobject=None
        return redirect('signup')

    if request.method =='POST' and 'submituserdetails' in request.POST: # Post the User Personal details
        isDefaultImage=False
        form = UserDetailsForm(request.POST)
        if form.is_valid(): 
            print("UserDetails are valid")
            

            # get the details from form 
            firstname=form.cleaned_data.get('firstname')
            lastname=form.cleaned_data.get('lastname')
            userId=userobject
            dob=form.cleaned_data.get('dob')
            gender=form.cleaned_data.get('gender') 
            mobile=form.cleaned_data.get('mobile')
           

            try:
                # get the image data captured from Webcam
                imageurls=request.POST.get('userprofiledata') 
                if imageurls is not BLANK:

                    imageurls += '=' * (-len(imageurls) % 4)

                    imageurls=imageurls.replace("data:image/png;base64,","",1)
                    imageurls=imageurls.replace("data:image/jpeg;base64,","",1)
                    imageurls=bytes(imageurls, 'utf-8')

                    print("\n\n IMAGE DATA : ",imageurls)
                else:
                    imageurls=BLANK
            except:
                imageurls=BLANK

            if imageurls is not BLANK:  # if image data exists , then convert to png file and save
                b=base64.b64decode(imageurls)
                photo=Image.open(io.BytesIO(b))
                photo.save("app/static/usersprofiles/"+str(request.session['userId'])+'.png')   
                
                photo=str(request.session['userId'])+'.png'
            else:  # use the default image
                isDefaultImage=True
                photo= DEFAULT_IMAGE

            

            #####    get the details from the form
                
            email=userobject.email
            country=form.cleaned_data.get('country')
            state=form.cleaned_data.get('state')
            city=form.cleaned_data.get('city')
            union_council=form.cleaned_data.get('union_council')
            address=form.cleaned_data.get('address')
            postal_code=form.cleaned_data.get('postal_code')
            smoking=form.cleaned_data.get('smoking')
            alchol=form.cleaned_data.get('alchol')
            previous_existing_history_diabets=form.cleaned_data.get('previous_existing_history_diabets')
            Hipertension=form.cleaned_data.get('Hipertension')
            Arthritis=form.cleaned_data.get('Arthritis')
            Allergies=form.cleaned_data.get('Allergies')
            Previous_Surgery=form.cleaned_data.get('Previous_Surgery')
            Any_Medication=form.cleaned_data.get('Any_Medication')
            BloodPressure=form.cleaned_data.get('BloodPressure')
            Temparature=form.cleaned_data.get('Temparature')
            HeratRate=form.cleaned_data.get('HeratRate')
            RespiratoryRate=form.cleaned_data.get('RespiratoryRate')
            Weight=form.cleaned_data.get('Weight')
            Height=form.cleaned_data.get('Height')
            try:
                files=request.FILES.getlist('images') # get the medical documents 
            except:
                files=[]
            
            print("\n\n",firstname,"\n\n",lastname,"\n\n",dob,"\n\n",gender,"\n\n",mobile,"\n\n",email,"\n\n",country,"\n\n",state,"\n\n",city,"\n\n",union_council,"\n\n",address,"\n\n",postal_code)
            print("\n",smoking,alchol,previous_existing_history_diabets,Hipertension,Arthritis,Allergies,Previous_Surgery)
            print("\n",Any_Medication,BloodPressure,Temparature,HeratRate,RespiratoryRate,Weight,Height)
            try:

                upload_medical_files(request,files) # upload medical documents
                
                userformdetails=UserDetails(Height=Height,Weight=Weight,RespiratoryRate=RespiratoryRate,HeratRate=HeratRate,Temparature=Temparature,BloodPressure=BloodPressure,Any_Medication=Any_Medication,Previous_Surgery=Previous_Surgery,Allergies=Allergies,Arthritis=Arthritis,Hipertension=Hipertension,smoking=smoking,alchol=alchol,previous_existing_history_diabets=previous_existing_history_diabets,userId=userId,firstname=firstname,lastname=lastname,dob=dob,gender=gender,email=email,mobile=mobile,photo=photo,country=country,state=state,city=city,union_council=union_council,address=address,postal_code=postal_code)
                userformdetails.save()  # save the User details Table object
              
                userobject.photo=userformdetails.photo
                userobject.save() # update the User photo 
                messages.add_message(request, messages.SUCCESS, ACCOUNT_ADDED)
            except:
                messages.add_message(request, messages.ERROR, SOMETHING_HAPPENED)

    elif request.method =='POST' and 'submitfamilydetails' in request.POST:  # post family details
        form2=FamilyDetailsForm(request.POST)
        if form2.is_valid(): 
            print("Family form details are valid")
            diseases=form2.cleaned_data.get('diseases')
            family_person_name=form2.cleaned_data.get('family_person_name')
            familyemail=form2.cleaned_data.get('familyemail')

            check_email_exits=check_if_email_alreadyexists(familyemail,request)  # check if family member email already exists
            if check_email_exits:
                messages.add_message(request, messages.ERROR, ACCOUNT_ALREADY_EXISTS)
            else: # if family member email doesnot exists, add it
                family=FamilyDetails(userId=userobject,diseases=diseases,family_person_name=family_person_name,familyemail=familyemail)
                family.save()
                
                messages.add_message(request, messages.SUCCESS,familyemail+ " "+ACCOUNT_ADDED)
        else:
            print("Family form details are not valid")
    elif request.method =='POST' and 'done' in request.POST:  # when click on the Done , Redirect to Dashboard
        return HttpResponseRedirect('/dashboard/')
    elif request.method =='POST' and 'interestsname' in request.POST:  # Add interest of user
        form3=InterestNamesForm(request.POST)
        if form3.is_valid():
            print("Interest Form is valid")

            interestname=form3.cleaned_data.get('interestname')
            try:
                innames=InterestNames.objects.all()
                exists=False
                for i in innames:
                    if i.name == interestname: # check if interest exists in User list
                        exists=True
                        print("Interest Exists")
                if not exists: # if not exists, add it
                    InterestNames(name=interestname).save()
                    Interests(name=interestname,userId=request.session['userId']).save()
                    update_interest_in_userdetails_table(request,interestname)
                    print("Interest not Exists, so insert")

            except:
                messages.add_message(request, messages.ERROR, SOMETHING_HAPPENED)
    
    
    try:
        # userdetails=User.objects.get(userId=request.session['userId'])
        form=UserDetailsForm()
        form2=FamilyDetailsForm()
        form3=InterestNamesForm()

        
            


        # setting the Email attribute value and non changeable
        form.fields["email"].initial=userobject.email
            
        print("Account Exists")
    except:
        userobject=None
        form=UserDetailsForm()
        form2=FamilyDetailsForm()
        form3=InterestNamesForm()

    template = loader.get_template('UserDetails.html')
    context = { 
        'form':form,
        'form2':form2,
        'form3':form3,
        "dictdata": json.dumps(getstates()),
        "diseases":json.dumps(getDiseases()),
        'form_list':get_family_details(request),
        'interests':InterestNames.objects.all(),

    }
    return HttpResponse(template.render(context, request))



# Return the Family details , if has any or recently added
def get_family_details(request):
    fdetails=[]
    try:
        fdetails=FamilyDetails.objects.filter(userId=request.session['userId'])
        print(fdetails)
    except:
        pass
    for i in fdetails:
        print(i.familyemail,"----",i.userId)
    return fdetails

# Used to split the image name and image format,( Never used ) 
def content_file_name(userId, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (userId, ext)
    return filename
   

# return the Country, state, City dropdown Values
def getstates():
    countries_dict={}
    state=[]
    counties=Country.objects.all()
    states = State.objects.all()
    cities=City.objects.all()
    
    for i in counties:
        state={}
        for j in states:
            citie=[]
            if j.country==i.name:
                for k in cities:
                    if k.state==j.name:
                        citie.append(k.name)
                state[j.name]=citie
        
        countries_dict[i.name]=state
    print(countries_dict)
    return countries_dict

# check if the Email alredy exists in Family table for User
def check_if_email_alreadyexists(familyemail,request):
    try:
        family=FamilyDetails.objects.get(familyemail=familyemail,userId=request.session['userId'])
        if family is None:
            print("Family member not exists")
            return False
        print("Family member exists")
        return True
    except:
        print("Family member not exists")
        return False

# Returns the Diseases/Specialization
def getDiseases():
    try:
        dict1={}
        dises=Diseases.objects.all()
        for i in dises:
            dict1[i.name]=i.name
        return dict1
    except:
        pass

# Upload Medical files/Documents  to DB
def upload_medical_files(request,files):
    try:
        for i in files:
            MedicalHistory(userId=request.session['userId'],photo=i).save()
    except:
        messages.add_message(request, messages.ERROR, SOMETHING_HAPPENED)

#  Add the Interest to Interest table , when Add interest is clicked
def interests(request,interest):
    try:
        interests=Interests.objects.get(name=interest)
        print("Interest Exits")
    except:
        interests=None
        print("No Interest Exists")

    if interests is None:
        Interests(name=interest,userId=request.session['userId']).save()
        update_interest_in_userdetails_table(request,interest)
        print("Inserting Interest")
    else:
        interests.delete()
        print("deleting existing Interest")
        remove_interest_in_userdetails_table(request,interest)
    return redirect('userdetails')
    
# when Interests are selected , will update the UserDetails Table for Interests
def update_interest_in_userdetails_table(request,interestname):

    try:
        userdetails_interest_object=UserDetails.objects.get(userId=request.session['userId'])
        if userdetails_interest_object and  interestname in str(userdetails_interest_object.interests):
            print("Interest already exists in userdetails")
        else:
            userdetails_interest_object.interests=str(userdetails_interest_object.interests)+"-"+interestname
            userdetails_interest_object.save()
    except:
        pass


# Remove the Interest from UserDetails , if they clicked on Interest that is alredy existed in UserDetails 
def remove_interest_in_userdetails_table(request,interestname):

    try:
        userdetails_interest_object=UserDetails.objects.get(userId=request.session['userId'])
        if userdetails_interest_object and  interestname in str(userdetails_interest_object.interests):
            userdetails_interest_object.interests=str(userdetails_interest_object.interests).replace("-"+interestname,"")
            userdetails_interest_object.save()
            print("Interest deleted from userdetails")
        else:
            print("Interest not exists in userdetails")
    except:
        pass


