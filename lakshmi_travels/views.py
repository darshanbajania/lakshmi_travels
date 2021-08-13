from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User, AnonymousUser
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
    return render(request, 'lakshmi_travels/index.html')

def TourPackagesView(request):
    return render(request, 'lakshmi_travels/tour_packages.html')

def DailyTripView(request):
    return render(request, 'lakshmi_travels/daily_trip.html')

def EnquiryPageview(request):
    return render(request, 'lakshmi_travels/enquiry_page.html')

def LoginView(request):
    return render(request, 'registration/login.html')

def RegisterView(request):
    return render(request, 'registration/register.html')

def CustomerDashboardView(request):
    return render(request, 'lakshmi_travels/customer_dashboard.html')

def AdminDashBoardView(request):
    return render(request, 'lakshmi_travels/admin_dashboard.html')
