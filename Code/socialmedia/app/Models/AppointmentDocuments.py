from django.db import models
from app.Models.User import User
from django.utils import timezone
from datetime import date, datetime
class AppointmentDocuments(models.Model):

    documents=models.FileField(upload_to='static/appointmentdocuments',blank=True)
    bookingid=models.CharField(max_length=100)