from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path


from app.Clinics import Clinic
urlpatterns = [
    path('', Clinic.index, name='clinic'),

    path('getall/',Clinic.filterall,name='filterclinicdoc'),

    path('clinicdetails/<clinicId>',Clinic.clinicdetails,name="clinicdetails"),
     
    path('doctordetails/<doctorId>',Clinic.doctordetails,name="doctordetails"),

    path('searchclinics/',Clinic.search_clinic,name='searchclinic'),
    path('getsearchedclinic/',Clinic.get_search_clinic,name='getsearchclinic'),

    path('doctordetails/getavailableslotsofday/',Clinic.getDoctorSlots,name='doctorslotsofday'),

    path('payment/',Clinic.makepayment,name="paymentsample"),
    path('payment/paymenthandler/', Clinic.paymenthandler, name='paymenthandler'),
   
    

   
    
]