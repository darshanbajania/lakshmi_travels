from django.http import request
from django.shortcuts import render, redirect

# Create your views here.


def Home(request):
    return render(request, 'lakshmi_travels/index.html')

def TourPackagesView(request):
    return render(request, 'lakshmi_travels/tour_packages.html')

def DailyTripView(request):
    return render(request, 'lakshmi_travels/daily_trip.html')

def EnquiryPageview(request):
    return render(request, 'lakshmi_travels/enquiry_page.html')
