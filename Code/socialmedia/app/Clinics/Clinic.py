
from datetime import datetime,date
from json import JSONDecodeError
import json
import os
import random
from django.conf import settings
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
from app.MessageHandler import SOMETHING_HAPPENED,WRONG_CODE_OR_ALREADY_USED,SLOT_SAVED,ERROR_IN_SLOT_SAVED,SLOT_ALREADY_BOOKED
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
from django.http import HttpResponseBadRequest
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from app.Models.Payment import Payment

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))



@csrf_protect
def index(request):  # Main page od clinic and Doctors Tabs Page

    # user=UserDetails.objects.filter(userId=request.session['userId'])
    if not request.session.has_key('userId') or request.session['userId']=='':
        return redirect("/")
    else:
        if request.method=='GET':

            deleteSessionVariables(request)

            template = loader.get_template('clinic_base.html')
            context = {
                'data':request.session['username']+" LoggedIN",
                'dictdata': json.dumps(getstates()),
                'special':json.dumps(getDiseases())
                }
            return HttpResponse(template.render(context, request))



# delete the Session Variables if Exists
def deleteSessionVariables(request):
    if request.session.has_key('amount') :
        del request.session['amount'] 
    if request.session.has_key('doctorId') :
        del request.session['doctorId'] 
    if request.session.has_key('paymentstatus') :
        del request.session['paymentstatus'] 
    if request.session.has_key('day') :
        del request.session['day'] 
    if request.session.has_key('timeofslot') :
        del request.session['timeofslot'] 
    if request.session.has_key('specialization') :
        del request.session['specialization'] 
    if request.session.has_key('couponcode') :
        del request.session['couponcode']
    if request.session.has_key('paymentmode') :
        del request.session['paymentmode'] 
    if request.session.has_key('couponamount') :
        del request.session['couponamount'] 
    

# this will returms the Country , State and City Dropdown data
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


# this will return the Avaialble Specializations/Diseases from Diseases Table
def getDiseases():
    try:
        dict1={}
        dises=Diseases.objects.all()
        for i in dises:
            dict1[i.name]=i.name
        return dict1
    except:
        pass

# Returns the Filtered Doctors and Clinics based on the Dropdown
def filterall(request):
    country=request.GET.get('country')
    state=request.GET.get('state')
    city=request.GET.get('city')
    spececilization=request.GET.get('spec')

    clinics=list(Clinic.objects.filter(country=country,state=state,city=city,specialization__icontains=spececilization).order_by("-rating").values('clinicId','clinicName','specialization','availability','clinicImage','rating'))
    doctors=list(Doctor.objects.filter(country=country,state=state,city=city,specialization__icontains=spececilization).order_by("-rating").values('doctorId','clinicId','doctorName','specialization','availabilityFrom','availabilityTo','doctorImage','rating'))

    dict={"clinics":clinics,"doctors":doctors}
    print("ALL Clinicns and Doctors",clinics,doctors)
    return JsonResponse(json.dumps(dict),safe=False)
    

# this will redirect to the Clinic details page where having clinic details and List of Doctors
def clinicdetails(request,clinicId):
    if not request.session.has_key('userId') or request.session['userId']=='':
        return redirect("/")
    else:
        clinics_object=Clinic.objects.filter(clinicId=clinicId).values()
        doctors_object=Doctor.objects.filter(clinicId=clinicId).values().order_by('experience','specialization')
        
        rating=0.0
        count=0
        for i in doctors_object:
            count=count+1
            rating=rating+i['rating']
        if count>0:
            rating=rating/count
        
        deleteSessionVariables(request)

        template = loader.get_template('clinic_details.html')
        context = {
                'user':request.session['username']+" LoggedIN",
                'clinic': clinics_object,
                'doctors':doctors_object,
                'rating':rating
                }
        return HttpResponse(template.render(context, request))
        

# this is Redirection page , where we will calculate the amount based on coupon and display details and Pay button
def makepayment(request):
    print("\nAt Make Payment Page Redirection\n\n")

    currency = 'INR'
	# amount = 200*100 # Rs. 200
    amount=int(request.session['amount'])*100

	# Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))

   

	# order id of newly created order.
	
    razorpay_order_id = razorpay_order['id']

    try:
        payment=Payment(paymentorderId=razorpay_order_id,amount=(amount/100),doctorId=request.session['doctorId'],userId=request.session['userId'],createdDate=timezone.now(),updatedDate=timezone.now())
        payment.save()
    except:
        messages.add_message(request, messages.ERROR, ERROR_IN_SLOT_SAVED)
        



	
    callback_url = 'paymenthandler/'

	# we need to pass these details to frontend.
	
    context = {}
    context['couponamount']=request.session['couponamount']
    context['finalamount']=request.session['amount']
    context['actualamount']=int(request.session['amount'])+int(request.session['couponamount'])
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    context['email']=request.session['email']
    context['username']=request.session['username']
    context['photo']=request.session['photo']

    return render(request, 'payment.html', context=context)
    



# If Appointment is direct consultaion , book the slot details 
def saveSlotDetails(request,amount,doctorId,paymentStatus,day,timeofslot,specialization,couponcode,paymentmode):
    doctor_bookings=None
    try:
        doctor_bookings=DoctorBooking.objects.get(doctorId=doctorId,dateofslot=day,slotTime=timeofslot)
        print("SLot Available: ",doctor_bookings)
        if doctor_bookings is not None or not []:
            messages.add_message(request, messages.ERROR, SLOT_ALREADY_BOOKED)
            return 
        else:
            pass
    except:
        pass
    try:
        doctorobject=Doctor.objects.get(doctorId=doctorId)
        print(doctorobject)
        slotbook_object=DoctorBooking(paymentmode=paymentmode,bookinguserId=request.session['userId'],doctorName=doctorobject.doctorName,amount=amount,doctorId=doctorobject,messageforanything="",paymentStatus=paymentStatus,dateofslot=day,slotTime=timeofslot,specialization=specialization,coupunused=couponcode,createdDate=timezone.now(),updatedDate=timezone.now())
        slotbook_object.save()
        messages.add_message(request, messages.ERROR, SLOT_SAVED)
    except:
        messages.add_message(request, messages.ERROR, ERROR_IN_SLOT_SAVED)

#if Appointment is Online, Save the Details in Session for Further referedces used in the Verification of Payment (Payment handler)
def savePaymentDetails(request,amount,doctorId,paymentstatus,day,timeofslot,specialization,couponcode,paymentmode,couponamount):
    request.session['amount'] = amount
    request.session['doctorId']= doctorId
    request.session['paymentstatus']=paymentstatus
    request.session['day'] = day.strftime("%Y-%m-%d")
    request.session['timeofslot']=timeofslot
    request.session['specialization']=specialization
    request.session['couponcode'] = couponcode
    request.session['paymentmode']=paymentmode
    request.session['couponamount']=couponamount

# this is a Doctor Details and Slot Booking Page  Redirection page
def doctordetails(request,doctorId):
    if not request.session.has_key('userId') or request.session['userId']=='':
        return redirect("/")
    else:
        
        if request.method=='POST':
            doctorslotform=BookDoctorSlotForm(request.POST)
            if doctorslotform.is_valid():
                couponcode=doctorslotform.cleaned_data.get('coupon')
                paymentmode=doctorslotform.cleaned_data.get('payment_mode')
                day=doctorslotform.cleaned_data.get('dateofslot')
                timeofslot=doctorslotform.cleaned_data.get('timeofslot')
                specialization=doctorslotform.cleaned_data.get('specialization')

                amount=float(request.POST.get('amount_input'))
                print("\n\nCOUPON CODE : ",couponcode)
                print("\n\nPAYMENT MODE: ",paymentmode)
                if couponcode!='' or couponcode.strip()!='': # if coupon is not Blank
                    coupon_object=None
                    try:
                        coupon_object=Coupon.objects.get(couponcode=couponcode)
                    except:
                        coupon_object=None

                    print("\n\n COUpon Object : ",coupon_object)
                    if coupon_object is None:  # if coupon is not valid and doesnot Exists
                        messages.add_message(request, messages.ERROR, WRONG_CODE_OR_ALREADY_USED)
                        if paymentmode=="Online":
                            savePaymentDetails(request,amount,doctorId,0,day,timeofslot,specialization,couponcode,paymentmode,0)
                            return redirect('paymentsample')
                        else:
                            saveSlotDetails(request,amount,doctorId,0,day,timeofslot,specialization,"",paymentmode)
                    else: #if coupon  exists
                        amount=amount-float(coupon_object.couponamount) # minus the coupon amount from actual amount
                        print("\n\nAmount: ",amount)
                        if paymentmode=="Online":
                            savePaymentDetails(request,amount,doctorId,0,day,timeofslot,specialization,couponcode,paymentmode,coupon_object.couponamount)
                            return redirect('paymentsample')
                        else:
                            saveSlotDetails(request,amount,doctorId,0,day,timeofslot,specialization,couponcode,paymentmode)
                else: # if coupon is Blank
                    print("\n\nAmount: ",amount)
                    if paymentmode=="Online": 
                        savePaymentDetails(request,amount,doctorId,0,day,timeofslot,specialization,couponcode,paymentmode,0)
                        return redirect('paymentsample')
                    else:
                        saveSlotDetails(request,amount,doctorId,0,day,timeofslot,specialization,couponcode,paymentmode)



        # GET code for Slot booking Page
        doctorslotform=BookDoctorSlotForm()
        user=None
        doctor=Doctor.objects.get(doctorId=doctorId)
        if doctor is not None:
            user=User.objects.get(userId=doctor.userId)
        
        starttime=doctor.availabilityFrom
        endtime=doctor.availabilityTo
        
        from datetime import date

        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        print("\n\nDate: ",d1)

        
        doctorslotform.fields["dateofslot"].initial=d1  # setting initial as today on loading the page
        
        deleteSessionVariables(request)

        template = loader.get_template('doctor_details.html')
        context = {
                'user':user,
                'doctor':doctor,
                'form':doctorslotform,
                'starttime':starttime,
                'endtime':endtime,
                'specilization':json.dumps((doctor.specialization).split(","))
                }
        return HttpResponse(template.render(context, request))



# gets the Available doctor slots from the DoctorBooking Table
def getDoctorSlots(request):

    dayofslot=request.GET.get('dateofslot')
    doctorId=request.GET.get('doctorId')
    starttime=request.GET.get('starttime')
    endtime=request.GET.get('endtime')
    specilization=request.GET.get('specilization')
    print("\n\nSpecilization:",specilization)

    amount_object=Amount.objects.get(doctorId=doctorId,specilization=specilization)
    
    doctor_bookings=DoctorBooking.objects.filter(doctorId=doctorId,dateofslot=dayofslot)
        
    specilization=specilization.split(",")
    listof_times=[]

    x = datetime.now()

    timenow=x.strftime("%X")[:2]

    # Generate all times from start to end time with difference of half-an-hour
    for i in range(int(starttime[:2])*2,int(endtime[:2])*2):
        listof_times.append("%02d:%s0"[:57-i]%(i/2,i%2*3))

    newlistoftimes=[]
    # For loop checks for the available Times for today or other days
    for i in listof_times:
        print("Time : ",timenow," Slot Time: ",i[:2])
        print("Date of Slot : ",dayofslot," Today Date: ",date.today())
        if dayofslot==str(date.today()) and int(i[:2])>int(timenow):
            newlistoftimes.append(i)
        elif dayofslot!=str(date.today()):
            newlistoftimes.append(i)
        else:
            continue
        
        
    # Check if slots are in Doctor list, if Yes dont add to list and dont display to user
    for i in doctor_bookings:
        slot=i.slotTime
        if slot in newlistoftimes:
            newlistoftimes.remove(slot)

    print("\n\nList of Times Doctor available :",newlistoftimes)
    return JsonResponse({'status':200,'data':json.dumps(newlistoftimes),'amount':json.dumps(amount_object.amount)})


# this is is the Search Functionality , which returms doctors and clinics
def search_clinic(request):
    postname=request.GET.get('clinicname')
    payload=[]
    searchpostIds=[]
    allpostobjects=[]
    if postname:
        postobjects=Clinic.objects.filter(clinicName__icontains=postname)
        doctobjects=Doctor.objects.filter(doctorName__icontains=postname)
        for i in postobjects:
            payload.append(i.clinicName)
           
        for j in doctobjects:
            payload.append(j.doctorName+"  (DOCTOR)")

    print("SEARCHED Data",allpostobjects)
    return JsonResponse({'status':200,'data':payload})

# onclicked on the Searched Doctor or clinic this will return the Id of the Searched thing
def get_search_clinic(request):
    postname=request.GET.get('clinicname')
    
    if "(DOCTOR)" in postname:
        postname=postname.replace("  (DOCTOR)", "")
        print("DOCTOR NAME",postname)
        postobjects=Doctor.objects.get(doctorName=postname)
        print(postobjects)
        return JsonResponse({'status':200,'data':postobjects.doctorId,'isDoctor':1})
    else:
        print("CLINIC NAME",postname)
        postobjects=Clinic.objects.get(clinicName=postname)
        print(postobjects)
        return JsonResponse({'status':200,'data':postobjects.clinicId,'isDoctor':0})
    


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        # try:
            # get th required parameters from the post request
        payment_id=request.POST.get('razorpay_payment_id','')
        razorpay_order_id=request.POST.get('razorpay_order_id','')
        signature=request.POST.get('razorpay_signature','')
        # amount=int(request.session['amount'])*100
        amount=(request.session['amount'])*100

        razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        params_dict={
            'razorpay_order_id':razorpay_order_id,
            'razorpay_payment_id':payment_id,
            'razorpay_signature':signature
        }

        print("\n\n Payment Handler Page AMount : ",amount,params_dict)

        # result= razorpay_client.utility.verify_payment_signature(params_dict)
        payment_object=None
        payment_object=Payment.objects.get(paymentorderId=razorpay_order_id)
        if payment_object is not None and payment_object.paymentorderId==razorpay_order_id:
    
            amount=amount
            try:
                # capture the Payment
                razorpay_client.payment.capture(payment_id,amount)
                # render Succes page

                saveSlotDetails(request,(amount/100),request.session['doctorId'],1,request.session['day'],request.session['timeofslot'],request.session['specialization'],request.session['couponcode'] ,request.session['paymentmode'])
                slotbook_object=DoctorBooking.objects.get(doctorId=request.session['doctorId'],dateofslot=request.session['day'],slotTime=request.session['timeofslot'],paymentStatus=1)
                doctorbookingid=slotbook_object.doctorbookingid

                payment_object.doctorbookingid=doctorbookingid
                payment_object.updatedDate=timezone.now()
                payment_object.save()


                messages.add_message(request, messages.SUCCESS, "Payment Success")
            except:
                messages.add_message(request, messages.ERROR, "Payment Failed")
            return redirect('doctordetails',doctorId=request.session['doctorId'])
        else:
            messages.add_message(request, messages.ERROR, "Payment Verification Failed")
            return redirect('doctordetails',doctorId=request.session['doctorId'])
        # except:
        #     print("Exception at Handler")
        #     return HttpResponseBadRequest()
    else:
        print("POST Method Failed at Handler")
        return HttpResponseBadRequest()
    



