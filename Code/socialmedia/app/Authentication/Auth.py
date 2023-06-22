from audioop import reverse
from base64 import urlsafe_b64decode, urlsafe_b64encode
import datetime
import random
import time
from datetime import date, timedelta
from django.contrib.auth.hashers import make_password,check_password
from readline import get_current_history_length
import string
from django.utils import timezone
import threading
from django.template import RequestContext, loader
from django.utils.html import format_html
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm
from django.shortcuts import redirect, render
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_protect
from app.Models.Followers import Contributers
from app.Models.Likes import Likes
from app.Models.Post import Post 
from app.Models.User import User
from app.Models.UserDetails import UserDetails
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from app.MessageHandler import DEFAULT_IMAGE,BLANK,ACCOUNT_DOES_NOT_EXISTS,PASSWORD_WRONG,PASSWORD_VALIDATIONS,LINK_EXPIRED,PASSWORD_RESET_SUCCESS,EMAIL_SUBJECT,EMAIL_FORGOT_PASSWORD,PLEASE_PROVIDE_USERNAME,PLEASE_VERIFY_EMAIL, PLEASE_PROVIDE_PASSWORD,EMAIL_VERIFY_SUCCESS,PASSWORD_MISMATCH,EMAIL_SEND_TO_USER,USER_ALREADY_VERIFIED,USER_ALREADY_REGISTERED
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
import re
from app.Models.DoctorBooking import DoctorBooking




@csrf_protect
def index(request): # Main Route for Login Pages
    form=UserForm()
    form1=UserLoginForm()
    form2=ForgotPasswordForm()



    ##########################################
    find_appointments_in_oneday_before(request)  # Find the Appointments and send email notofication , Placed here for Sample
    ##########################################



    request.session['userId'] = BLANK
    request.session['username']= BLANK

    if 'signup' in request.POST and request.method=='POST':  # Signup form

        
        form = UserForm(request.POST)
    
        if form.is_valid():
            print('\n\nSignup Form is Valid -----------------')
            password=form.cleaned_data.get('password')
            repassword=form.cleaned_data.get('repassword')
            email=form.cleaned_data.get('email') 
            username=form.cleaned_data.get('username')
            print('\n\n\nUsername:',username ,"\n\n\n")
            if password !=repassword :
                messages.add_message(request, messages.ERROR, PASSWORD_MISMATCH)
            else:
               
                res,res2=checkPasswordRegularExpretionMatch(password,repassword)
                
                if not res and not res2:
                    messages.add_message(request, messages.ERROR, PASSWORD_VALIDATIONS)
                else:
                    if username==BLANK:
                        messages.add_message(request, messages.ERROR, PLEASE_PROVIDE_USERNAME)
                    elif password==BLANK or repassword==BLANK:
                        messages.add_message(request, messages.ERROR, PLEASE_PROVIDE_PASSWORD)
                    elif password !=repassword :
                        messages.add_message(request, messages.ERROR, PASSWORD_MISMATCH)
                    else:
                        isExists,isVerified=check_if_user_exists(email)
                        if isExists :
                            # if User is Old
                            messages.add_message(request, messages.ERROR, USER_ALREADY_REGISTERED)
                        else:
                            # if User is New , Send a Mail
                            token=str(random.random()).split(".")[1].join(random.choices(string.ascii_uppercase +string.digits, k = 10))+str(datetime.datetime.now())
                            user=User(photo=DEFAULT_IMAGE,username=username,email=email,password=make_password(password),isProfileActive=False,isVerified=False,token=token)
                            user.save()
                            send_email_to_verify(email,token,request,EMAIL_SUBJECT,'account_activate.html')
        else:
            form=UserForm()

        

        
    elif 'login' in request.POST and request.method=='POST':   # LoginForm
        form1=UserLoginForm(request.POST)
        if form1.is_valid():
            print('\n\nLogin Form is Valid -----------------')
            password=form1.cleaned_data.get('password')
            email=form1.cleaned_data.get('email') 
            if password==BLANK:
                messages.add_message(request, messages.ERROR, PLEASE_PROVIDE_PASSWORD)
            else:
                check_for_the_user_to_login(request,email,password)
        else:
            form1=UserLoginForm()
        
        
    elif 'passwordreset' in request.POST and  request.method=='POST':  # Password ResetForm
        form2=ForgotPasswordForm(request.POST)
        if form2.is_valid():
            email=form2.cleaned_data.get('email') # get the email and Generate a Token
            token=str(random.random()).split(".")[1].join(random.choices(string.ascii_uppercase +string.digits, k = 10))+str(datetime.datetime.now())
            try:
                user=User.objects.get(email=email)
                if user and user.isVerified:
                    # if User is Exists and Verified, SAVE the token in DB for further purposes
                    token=str(random.random()).split(".")[1].join(random.choices(string.ascii_uppercase +string.digits, k = 10))+str(datetime.datetime.now())
                    user.token=token
                    user.save()
                    send_email_to_verify(email,token,request,EMAIL_FORGOT_PASSWORD,'password_reset.html')
                else:
                    # if not Verified 
                    messages.add_message(request, messages.ERROR, PLEASE_VERIFY_EMAIL)
            except:
                # if User does not Exists
                user=None
                messages.add_message(request, messages.ERROR, ACCOUNT_DOES_NOT_EXISTS)
        else:
            form2=ForgotPasswordForm()
        

    # GET code is here
    if request.session['username'] is not BLANK:
        try:
            # Checks if the User is LoggedIn first Time
            userdetails=UserDetails.objects.get(userId=request.session['userId'])
        except:
            userdetails=None
        if userdetails is None:
            # if User is First Time , Redirect to User Details Page
            print("No User Details Found, Redirct to UserDetails Page")
            return HttpResponseRedirect('/profile/userdetails/')
        
        # if User is Not first time
        return HttpResponseRedirect('/post/')
    template = loader.get_template('signup.html')
    context = { 
        'form':form,
        'form1':form1,
        'form2':form2
    }
    return HttpResponse(template.render(context, request))


# This is the route where Reset Password is Accesssed from Email Link
def reset_password(request,uid64,token):
    form4=ResetPasswordForm()
    if request.method=='POST' :
        form4=ResetPasswordForm(request.POST)
        if form4.is_valid():
            password=form4.cleaned_data.get('password')
            repassword=form4.cleaned_data.get('repassword')

            res,res2=checkPasswordRegularExpretionMatch(password,repassword)
            if not res and not res2:
                messages.add_message(request, messages.ERROR, PASSWORD_VALIDATIONS)
            else:
                print(password," ++ ",repassword)
                if password==BLANK or repassword==BLANK:
                    messages.add_message(request, messages.ERROR, PLEASE_PROVIDE_PASSWORD)
                elif password !=repassword :
                    messages.add_message(request, messages.ERROR, PASSWORD_MISMATCH)
                elif password == repassword :
                    try:
                        email=force_str(urlsafe_base64_decode(uid64))
                        user=User.objects.get(email=email)
                        if user and token==user.token:
                            user.token=BLANK
                            user.password=password
                            user.updatedDate=datetime.datetime.now()
                            user.save()
                            messages.add_message(request, messages.SUCCESS, PASSWORD_RESET_SUCCESS)
                            # return render(request,'sample.html',{'data':PASSWORD_RESET_SUCCESS})
                            return HttpResponseRedirect('/home')
                        else:
                            return render(request,'sample.html',{'data':LINK_EXPIRED})
                    except:
                        user=None
                        messages.add_message(request, messages.SUCCESS, ACCOUNT_DOES_NOT_EXISTS)
            

    return render(request,'forgotpassword.html',{'formforgot':form4})
    




# this is the route for Activate Account by Email Verification , where user access page from email link
def activate_account(request,uid64,token):
    try:
        email=force_str(urlsafe_base64_decode(uid64))
        user=User.objects.get(email=email)
    except Exception as e:
        user=None
    if user and user.token==BLANK:
        return HttpResponse(USER_ALREADY_VERIFIED)
    if user and token==user.token:
        user.isVerified=True
        user.token=BLANK
        user.updatedDate=datetime.datetime.now()
        user.save()
        return render(request,'sample.html',{'data':EMAIL_VERIFY_SUCCESS})
    return render(request,'account_activate_fail.html',{'user':email})




# checks if the user is already Registered or not and returns True, True if Exists,Verified
def check_if_user_exists(email):
    try:
        user=User.objects.get(email=email)
        if user is not None:
            return True,user.isVerified
        return False,user.isVerified
    except :
        return False,False


# Sending Email by providing the all the required feilds
def send_email_to_verify(email,token,request,email_subject,render_to_stringfile):
    current_site=get_current_site(request) # gets the domain
    email_subject=email_subject
    email_body=render_to_string(render_to_stringfile,{
        'email':email,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(email)),
        'token':token
    })
    
    email=EmailMessage(email_subject,email_body,from_email=settings.EMAIL_FROM_USER,to=[email])
    email.content_subtype = 'html'
    EmailThread(email).start()
    messages.add_message(request, messages.SUCCESS, EMAIL_SEND_TO_USER)


# Delete Users method ( Never Used anywhere, used for testing)
def delallusers():
    member = User.objects.all()
    member.delete()


# Thread Class used to Send Mails as individual
class EmailThread(threading.Thread):
    def __init__(self,email):
        self.email=email
        threading.Thread.__init__(self)
    def run(self):
        self.email.send()




# This Method is used for, if user is registered and verified to Login or Not
def check_for_the_user_to_login(request,email,password):
    print("Came to check user to login")
    try:
        user=User.objects.get(email=email)
        print("User Found")
    except Exception as e:
        print("User Not found ")
        # messages.add_message(request, messages.ERROR, ACCOUNT_DOES_NOT_EXISTS)
        messages.error(request,ACCOUNT_DOES_NOT_EXISTS)
        user=None
        return None
    if user and not user.isVerified:
        messages.add_message(request, messages.ERROR, PLEASE_VERIFY_EMAIL)
    elif user and check_password(password,user.password) and user.isVerified:
        print("Hello World",user.isVerified)
        request.session['userId'] = user.userId
        request.session['username']=user.username
        request.session['photo']=user.photo
        request.session['email']=user.email

        user.isProfileActive=True
        user.lastlogin=timezone.now()
        user.save()
    else:
        print("Wrong Password")
        # messages.add_message(request, messages.ERROR, PASSWORD_WRONG)
        messages.error(request,PASSWORD_WRONG)
    


 # checking for PAssword Regular Expression MAtch, returns True or False
def checkPasswordRegularExpretionMatch(passw,repassw):
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"
    match_re = re.compile(reg)
    res = re.search(match_re, passw)
    res2=re.search(match_re,repassw)
    return res,res2


#logout and save Lastlogin Time and redirects to Main Login page
def logout(request):
    del request.session['userId'] 
    del request.session['username']

    user=User.objects.get(email=request.session['email'])
    user.isProfileActive=0
    user.lastlogin=timezone.now()
    user.save()
    
    return redirect("/post")








# Last Two Months Logic can be removed from this Class and can implement as you required
def get_allrecords_of_posts_in_last_two_months():

    date1=datetime.datetime.now() + timedelta(days=-60)

    # get all record of last two months
    post_records=Post.objects.filter(updatedDate__lte=date1)
    print("\n\nLAst two Months {} Records :{}",date1,post_records)

    if len(post_records) > 0:
        for i in post_records:
            likes_records=Likes.objects.filter(postId=i.postId,updatedDate__range=[date1,timezone.now()])
        
            print("\nLikes :",likes_records)
            if len(likes_records) == 0:
                print("\nLikes : NO")
                contributers=Contributers.objects.filter(postId=i.postId,updatedDate__range=[date1,timezone.now()])

                print("\nContributers: ",contributers)

                if len(contributers) == 0:
                    print("\Contributers : NO")
                    i.isActive=-1
                    i.updatedDate=timezone.now()
                    i.save()
                else:
                    print("\Contributers : YES")
                    continue
            else:
                print("\nLikes : YES")
                continue
    else:
        return



# find the Appointments one day before and send email Notifications
def find_appointments_in_oneday_before(request):
    date1=date.today() + timedelta(days=1)
    current_site=get_current_site(request) # gets the domain
    appointsments=DoctorBooking.objects.filter(dateofslot=date1)
    for i in appointsments:
        user=User.objects.get(userId=i.bookinguserId)
        if user is not None:
            email_subject="Remainder for the Doctor Appointment "
            email_body=render_to_string("DoctorAppointment.html",{
                'email':user.email,
                'domain':current_site,
                'username':user.username,
                'date':i.dateofslot,
                'time':i.slotTime
                
            })
            
            email=EmailMessage(email_subject,email_body,from_email=settings.EMAIL_FROM_USER,to=[user.email])
            email.content_subtype = 'html'
            EmailThread(email).start()
    print("\n\nAppointments : ",appointsments,date1)



# get_allrecords_of_posts_in_last_two_months()
