from django.http import request
from django.shortcuts import render, redirect
from .models import TripDetails, RentalCars
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User, AnonymousUser
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
import datetime
from django.utils.timezone import utc
from django.http import JsonResponse
import json


# Create your views here.


def Home(request):
    all_rental_cars = RentalCars.objects.all()
    all_daily_trips = TripDetails.objects.all()
    first_few_trips = all_daily_trips[:4]
    booking_type = 'tour'

    print(first_few_trips)
    if request.method == 'POST':
        booking_request_rental_car_id = request.POST.get('car_rental_id')
        trip_booking_request_id = request.POST.get('trip_id')
        if booking_request_rental_car_id != None:
            booking_type = 'rental_car'
            base_url = reverse('lakshmi_travels:enquiry_page')
            query_string = urlencode({'rental_car_id': booking_request_rental_car_id, 'booking_type': booking_type})
            url = '{}?{}'.format(base_url, query_string)
        elif trip_booking_request_id != None:
            booking_type = 'trip'
            base_url = reverse('lakshmi_travels:enquiry_page')
            query_string = urlencode({'rental_car_id': trip_booking_request_id, 'booking_type': booking_type})
            url = '{}?{}'.format(base_url, query_string)            
        # print(url)
        return redirect(url)


    context = {
        'all_rental_cars': all_rental_cars,
        'first_few_trips': first_few_trips,
    }

    return render(request, 'lakshmi_travels/index.html', context)

def TourPackagesView(request):
    return render(request, 'lakshmi_travels/tour_packages.html')

def DailyTripView(request):

    return render(request, 'lakshmi_travels/daily_trip.html')

def EnquiryPageview(request):
    booking_type = request.GET.get('booking_type')
    
    print(booking_type)
    # car_request_id = request.GET.get('rental_car_id')
    car_request_id = '1'
    selected_car = RentalCars.objects.all().filter(car_id = car_request_id).first()
    if selected_car!= None:
        booking_type = 'rental_car'
    
    context = {
        'booking_type': booking_type,
        'selected_car': selected_car,
    }
    return render(request, 'lakshmi_travels/enquiry_page.html', context)

def LoginView(request):
    if request.method == 'POST':
        login_username = request.POST.get('username')
        login_password = request.POST.get('password')
        # print(login_username, login_password)

        user = authenticate(username=login_username, password=login_password)
        print(user)

        if user is not None:
            login(request, user)
            request.session['is_logged_in'] = True
            return redirect('/')

    return render(request, 'registration/login.html')

def RegisterView(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

    context = {
        'form': form,
    }
    return render(request, 'registration/register.html', context)

@login_required
def CustomerDashboardView(request):
    return render(request, 'lakshmi_travels/customer_dashboard.html')

@login_required
def AdminDashBoardView(request):
    return render(request, 'lakshmi_travels/admin_dashboard.html')
