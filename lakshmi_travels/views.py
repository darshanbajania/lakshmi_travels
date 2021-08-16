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

    context = {
        'all_rental_cars': all_rental_cars,
    }

    return render(request, 'lakshmi_travels/index.html', context)

def TourPackagesView(request):
    return render(request, 'lakshmi_travels/tour_packages.html')

def DailyTripView(request):
    return render(request, 'lakshmi_travels/daily_trip.html')

def EnquiryPageview(request):
    return render(request, 'lakshmi_travels/enquiry_page.html')

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
