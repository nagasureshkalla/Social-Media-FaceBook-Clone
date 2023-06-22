
from audioop import reverse
from base64 import urlsafe_b64decode, urlsafe_b64encode
import datetime
import imp
import random
import json,os
import time
from turtle import hideturtle
from django.contrib.auth.hashers import make_password,check_password
from readline import get_current_history_length
import string
import threading
from django.http import HttpResponse, JsonResponse
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
from app.MessageHandler import SOMETHING_HAPPENED,ACCOUNT_ALREADY_EXISTS,ACCOUNT_ADDED
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
from app.Models.Post import Post

@csrf_protect
def index(request):
    # Dashboard page 
    if not request.session.has_key('userId') or request.session['userId']=='':
        return redirect("/")
    else:
        template = loader.get_template('Dashboard.html')
        context = { 
            'user':request.session['userId'],
        
        }
        return HttpResponse(template.render(context, request))


