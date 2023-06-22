from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from app.MyAppointments import MyAppointments


urlpatterns = [
    path('', MyAppointments.index, name='myappointments'),
    path('doctorappointmentviewdetails/<bookingid>',MyAppointments.appointmentDetails,name='doctorappointmentviewdetails'),
    path('rating/',MyAppointments.Rating,name='appointmentrating'),
    path('cancelappointment/',MyAppointments.cancelAppointment,name='cancelappointment'),
    
]+static(settings.MEDIA_URL,Document_riit=settings.MEDIA_ROOT)