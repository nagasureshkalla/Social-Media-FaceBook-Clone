
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
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_protect 
from django.http import HttpResponse, JsonResponse
from app.MessageHandler import SOMETHING_HAPPENED,REFUND,APPOINTMENT_CANCELD,APPOINTMENT_CANCEL_FAILED,WRONG_CODE_OR_ALREADY_USED,SLOT_SAVED,ERROR_IN_SLOT_SAVED,SLOT_ALREADY_BOOKED
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
from app.Models.DoctorBooking import DoctorBooking
from app.Clinics.BookDoctorSlotForm import BookDoctorSlotForm
from app.Models.Amount import Amount
from app.Models.Coupon import Coupon
from app.MyAppointments.DocumentsForm import DocumentForm
from app.Models.AppointmentDocuments import AppointmentDocuments
from app.Models.Payment import Payment


@csrf_protect
def index(request):   # Main page for Myappointments of upcoming and Past 

    # user=UserDetails.objects.filter(userId=request.session['userId'])
    if not request.session.has_key('userId') or request.session['userId']=='':
        return redirect("/")
    else:
        if request.method=='GET':

            todaydate=datetime.today().strftime('%Y-%m-%d')
            time=datetime.now().strftime("%H:%M")
            print("\n\nTODAY DATE : ",todaydate,time)

            booking_details=DoctorBooking.objects.filter(bookinguserId=request.session['userId']).order_by('dateofslot','slotTime').values()

            pastappointments=[]
            upcomingappointments=[]

            for i in booking_details:
                
                if i['dateofslot'].strftime('%Y-%m-%d') >= todaydate and i['appointmentstatus']!=1 :  # checks if appointment dat is today,tommorow ,...
                    upcomingappointments.append(i)  
                else:    # past appointments
                    pastappointments.append(i)

            print("UPcoming : ",upcomingappointments,"\n\nPast : ",pastappointments)

            template = loader.get_template('myappointments.html')
            context = {
                
                'pastappointments':pastappointments,
                 'upcomingappointments':upcomingappointments,
                 'upcomingtotal':len(upcomingappointments),
                 'pasttotal':len(pastappointments),
                 'todaydate':todaydate,
                 'time':time
                  
                
                }
            return HttpResponse(template.render(context, request))


# this is the Page redirection fro Appointment Details, where chat for doctor and user exists
def appointmentDetails(request,bookingid):
    if not request.session.has_key('userId') or request.session['userId']=='':
        return redirect("/")
    else:

            
        booking_details=DoctorBooking.objects.get(doctorbookingid=bookingid)

        if request.method =='POST':  # publish the Document shared by user to doctor
            documentform = DocumentForm(request.POST)
            if documentform.is_valid():
                files=[]
                try:
                    files=request.FILES.getlist('documents')    
                except:
                    files=[]
                upload_doctorappointment_files(request,files,bookingid)



        # GET the Appointment details Page
        documentform=DocumentForm()
        bookingid="DoctorAppointment-"+bookingid
        template = loader.get_template('viewappointmentdetails.html')
        context = {
            
        'bookingid':bookingid,
        'userId':request.session['userId'],
        'documentform':documentform,
        'message':booking_details.messageforanything
                
        }
        return HttpResponse(template.render(context, request))


# Submit the Rating for the Doctor Appointment
def Rating(request):
    if not request.session.has_key('userId') or request.session['userId']=='':
        return redirect("/")
    else:

        try:
            rating=request.GET.get('rating')
            bookingid=request.GET.get('bookingid')

            print("Rating : ",rating," BookingID : ",bookingid)

            appointment_object=DoctorBooking.objects.get(doctorbookingid=bookingid)

            appointment_object.rating=rating

            appointment_object.save()

            return JsonResponse({'status':200,'data':1})
        except:
            return JsonResponse({'status':200,'data':0})

# upload the documents in the Doctor appointment Chat page
def upload_doctorappointment_files(request,files,bookingid):

    try:
        for i in files:
            AppointmentDocuments(bookingid=bookingid,documents=i).save()
    except:
        messages.add_message(request, messages.ERROR, SOMETHING_HAPPENED)


# Cancel the Appointment 
def cancelAppointment(request):

    try:
        bookingId=request.GET.get('bookingid')
        appointment_object=DoctorBooking.objects.get(doctorbookingid=bookingId)
        appointment_object.appointmentstatus=-1
        appointment_object.save()

        if appointment_object.paymentmode=="Online" and appointment_object.paymentStatus==1:
            payment_object=Payment.objects.get(doctorbookingid=bookingId)
            payment_object.refundStatus=1
            payment_object.save()
            messages.add_message(request, messages.ERROR, REFUND)

        messages.add_message(request, messages.ERROR, APPOINTMENT_CANCELD)
        return JsonResponse({'status':200,'data':1})
    except:
        messages.add_message(request, messages.ERROR, APPOINTMENT_CANCEL_FAILED)
        return JsonResponse({'status':200,'data':0})
