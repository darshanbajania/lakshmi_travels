from django.http import request
from django.shortcuts import render, redirect
from .models import TripDetails, RentalCars, Customers
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
from django.core.mail import send_mail

from django.utils.timezone import utc
from django.http import JsonResponse
import json


# Create your views here.


def Home(request):
    all_rental_cars = RentalCars.objects.all().filter(availabilty_status = True)
    all_daily_trips = TripDetails.objects.all()
    first_few_trips = all_daily_trips[:4]
    booking_type = 'tour'
    # print(request.user.is_staff)
    if request.method == 'POST':
        booking_request_rental_car_id = request.POST.get('car_rental_id')
        trip_booking_request_id = request.POST.get('trip_id')
        daily_trip_route = request.POST.get('routes')
        daily_trip_date = request.POST.get('daily_trip_date')
        if booking_request_rental_car_id != None:
            booking_type = 'rental_car'
            base_url = reverse('lakshmi_travels:enquiry_page')
            query_string = urlencode({'rental_car_id': booking_request_rental_car_id, 'booking_type': booking_type})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)

        elif trip_booking_request_id != None:
            booking_type = 'daily_trip'
            base_url = reverse('lakshmi_travels:enquiry_page')
            query_string = urlencode({'daily_trip_id': trip_booking_request_id, 'booking_type': booking_type})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
        elif daily_trip_route != None:
            print(daily_trip_route)
            base_url = reverse('lakshmi_travels:daily_trip')
            query_string = urlencode({'daily_trip_route': daily_trip_route, 'daily_trip_date': daily_trip_date})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
        # print(url)


    context = {
        'all_rental_cars': all_rental_cars,
        'first_few_trips': first_few_trips,
    }

    return render(request, 'lakshmi_travels/index.html', context)

def TourPackagesView(request):
    return render(request, 'lakshmi_travels/tour_packages.html')

def DailyTripView(request):
    daily_trip_route = request.GET.get('daily_trip_route')
    daily_trip_date = request.GET.get('daily_trip_date')
    selected_day_trip = TripDetails.objects.all().filter(route = daily_trip_route, trip_timings__date = daily_trip_date)

    if request.method == "POST":
        trip_booking_request_id = request.POST.get('trip_id')
        daily_trip_route = request.POST.get('routes')
        daily_trip_date = request.POST.get('daily_trip_date')
        if trip_booking_request_id != None:
            booking_type = 'daily_trip'
            base_url = reverse('lakshmi_travels:enquiry_page')
            query_string = urlencode({'daily_trip_id': trip_booking_request_id, 'booking_type': booking_type})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
        elif daily_trip_route != None:
            print(daily_trip_route)
            base_url = reverse('lakshmi_travels:daily_trip')
            query_string = urlencode({'daily_trip_route': daily_trip_route, 'daily_trip_date': daily_trip_date})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)    
    context = {
        'selected_day_trip': selected_day_trip,
    }
    
    print(selected_day_trip)

    return render(request, 'lakshmi_travels/daily_trip.html', context)

def EnquiryPageview(request):
    booking_type = request.GET.get('booking_type')
    daily_trip_id = request.GET.get('daily_trip_id')
    car_request_id = request.GET.get('rental_car_id')
    selected_car = None
    selected_trip = None
    # if request.method == "POST":
        
        # name = request.POST.get('name')
        # sender = request.POST.get('email_id')
        # mobile = request.POST.get('phone')
        # query = request.POST.get('message')
        # recipients = ['darshanbajania1999@gmail.com']
        # subject = "Website Inquiry"
        # message = "hello testing"
        # message = "Name: "+name + "\nEmail Id: "+ sender + "\nMobile No: "+ str(mobile) +"\nMessage: " + query
        # send_mail(subject, message, 'darshanbajania1999@gmail.com', recipients)
    if booking_type == 'rental_car':
        selected_car = RentalCars.objects.all().filter(car_id = car_request_id).first()
        if selected_car!= None:
            booking_type = 'rental_car'
    elif booking_type == 'daily_trip':
        selected_trip = TripDetails.objects.all().filter(trip_id = daily_trip_id).first()

    # print(booking_type, car_request_id, daily_trip_id)
    context = {
        'booking_type': booking_type,
        'selected_car': selected_car,
        'selected_trip': selected_trip,
    }
    return render(request, 'lakshmi_travels/enquiry_page.html', context)

def LoginView(request):
    if request.session.has_key('is_logged_in'):
        return redirect('/')
    else:
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
            return redirect('/')
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

@login_required
def AdminDashBoardCustomersView(request):
    all_users = User.objects.all()
    context = {
        'all_users': all_users,
    }
    print(all_users)
    return render(request, 'lakshmi_travels/admin_dashboard_customers.html', context)

@login_required
def AdminDashBoardToursView(request):
    return render(request, 'lakshmi_travels/admin_dashboard_tours.html')

@login_required
def AdminDashBoardRentalCarsView(request):
    all_rental_cars = RentalCars.objects.all()
    counter = 1
    if request.method == 'POST':
        for rental_car in all_rental_cars:
            
            car_data = request.POST.get('car_'+str(rental_car.car_id))
            if car_data == 'on':
                rental_car.availabilty_status = True
            else:
                rental_car.availabilty_status = False
            
            rental_car.save()
            print(rental_car.availabilty_status)

            # elif car_data == 
            # print(car_data)
            counter += 1
        car_data = request.POST
        print(request.POST)
    context = {
        'all_rental_cars': all_rental_cars,
    }
    return render(request, 'lakshmi_travels/admin_dashboard_rental_cars.html', context)
@login_required
def AdminDashBoardDailyTripsView(request):
    return render(request, 'lakshmi_travels/admin_dashboard_daily_trips.html')