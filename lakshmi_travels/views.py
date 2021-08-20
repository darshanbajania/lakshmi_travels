from django.db import router
from django.http import request
from django.shortcuts import render, redirect
from .models import TourPackageDetails, TripDetails, RentalCars, Customers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User, AnonymousUser
from .forms import CreateUserForm, TripDetailsForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from datetime import datetime
from django.core.mail import send_mail
from django.utils.timezone import utc
from django.utils import timezone
from django.http import JsonResponse
import pytz
import json


# Create your views here.


def Home(request):
    all_rental_cars = RentalCars.objects.all().filter(availabilty_status=True)
    all_daily_trips = TripDetails.objects.all()
    all_tour_packages = TourPackageDetails.objects.all()
    all_tour_packages = all_tour_packages[:3]

    first_few_trips = all_daily_trips[:4]
    booking_type = 'tour'
    # print(request.user.is_staff)
    if request.method == 'POST':
        if request.POST.get('contact-form') == 'contact-form':
            name = request.POST.get('full-name')
            sender = request.POST.get('email-id')
            # mobile = request.POST.get('phone')
            query = request.POST.get('message')
            recipients = ['darshanbajania1999@gmail.com']
            subject = "Lakshmi Travels Website Inquiry - Home page"
            message = "hello testing"
            message = "Name: "+name + "\nEmail Id: " + sender + "\nMessage: "
            send_mail(subject, message, 'darshanbajania1999@gmail.com', recipients)

        booking_request_rental_car_id = request.POST.get('car_rental_id')
        trip_booking_request_id = request.POST.get('trip_id')
        daily_trip_route = request.POST.get('routes')
        daily_trip_date = request.POST.get('daily_trip_date')
        if booking_request_rental_car_id != None:
            booking_type = 'rental_car'
            base_url = reverse('lakshmi_travels:enquiry_page')
            query_string = urlencode(
                {'rental_car_id': booking_request_rental_car_id, 'booking_type': booking_type})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)

        elif trip_booking_request_id != None:
            booking_type = 'daily_trip'
            base_url = reverse('lakshmi_travels:enquiry_page')
            query_string = urlencode(
                {'daily_trip_id': trip_booking_request_id, 'booking_type': booking_type})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
        elif daily_trip_route != None:
            print(daily_trip_route)
            base_url = reverse('lakshmi_travels:daily_trip')
            query_string = urlencode(
                {'daily_trip_route': daily_trip_route, 'daily_trip_date': daily_trip_date})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)

        if request.POST.get('tour_request_type') == 'details':
            tour_package_id = request.POST.get('tour_id')
            base_url = reverse('lakshmi_travels:tour_package_details')
            query_string = urlencode(
                {'tour_package_id': tour_package_id})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)

        if request.POST.get('tour_request_type') == 'enquiry':
            booking_type = 'tour_package'
            tour_package_id = request.POST.get('tour_id')
            base_url = reverse('lakshmi_travels:enquiry_page')
            query_string = urlencode(
                {'booking_type': booking_type, 'tour_package_id': tour_package_id})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)

        # print(url)

    context = {
        'all_rental_cars': all_rental_cars,
        'first_few_trips': first_few_trips,
        'all_tour_packages': all_tour_packages,

    }

    return render(request, 'lakshmi_travels/index.html', context)


def TourPackagesView(request):
    all_tour_packages = TourPackageDetails.objects.all()
    if request.method == "POST":
        if request.POST.get('tour_request_type') == 'details':
            tour_package_id = request.POST.get('tour_id')
            base_url = reverse('lakshmi_travels:tour_package_details')
            query_string = urlencode(
                {'tour_package_id': tour_package_id})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)

        if request.POST.get('tour_request_type') == 'enquiry':
            booking_type = 'tour_package'
            tour_package_id = request.POST.get('tour_id')
            base_url = reverse('lakshmi_travels:enquiry_page')
            query_string = urlencode(
                {'booking_type': booking_type, 'tour_package_id': tour_package_id})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
    context = {
        'all_tour_packages': all_tour_packages,
    }
    return render(request, 'lakshmi_travels/tour_packages.html', context)


def TourPackageDetailsView(request):
    package_id = request.GET.get('tour_package_id')
    selected_package = TourPackageDetails.objects.all().filter(tour_id=package_id).first()

    context = {
        'selected_package': selected_package,
    }
    return render(request, 'lakshmi_travels/tour_details.html', context)


def DailyTripView(request):
    daily_trip_route = request.GET.get('daily_trip_route')
    daily_trip_date = request.GET.get('daily_trip_date')
    selected_day_trip = TripDetails.objects.all().filter(
        route=daily_trip_route, trip_timings__date=daily_trip_date)

    if request.method == "POST":
        trip_booking_request_id = request.POST.get('trip_id')
        daily_trip_route = request.POST.get('routes')
        daily_trip_date = request.POST.get('daily_trip_date')
        if trip_booking_request_id != None:
            booking_type = 'daily_trip'
            base_url = reverse('lakshmi_travels:enquiry_page')
            query_string = urlencode(
                {'daily_trip_id': trip_booking_request_id, 'booking_type': booking_type})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
        elif daily_trip_route != None:
            print(daily_trip_route)
            base_url = reverse('lakshmi_travels:daily_trip')
            query_string = urlencode(
                {'daily_trip_route': daily_trip_route, 'daily_trip_date': daily_trip_date})
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
    tour_package_id = request.GET.get('tour_package_id')
    selected_car = None
    selected_trip = None
    selected_tour = None

    if request.method == "POST":
        print(request.POST.get('item-category'))

        if request.POST.get('item-category') == 'rental-car':
            car_model = request.POST.get('car_model')
            location = request.POST.get('location')
            date = request.POST.get('date')

            name = request.POST.get('full-name')
            sender = request.POST.get('email')
            mobile = request.POST.get('phone-number')

            recipients = ['darshanbajania1999@gmail.com']
            subject = "Lakshmi Travels website Enquiry: Rental Car / Registered"
            message = "hello testing"
            message = "Name: "+name + "\nEmail Id: " + sender + "\nMobile No: " + \
                str(mobile) + "\n\nCar Model: "+car_model + \
                "\nLocation: "+location + "\nDate: "+date
            send_mail(subject, message,
                      'darshanbajania1999@gmail.com', recipients)

        elif request.POST.get('item-category') == 'daily-trip':

            route = request.POST.get('route')
            location = request.POST.get('date')
            date = request.POST.get('location')

            name = request.POST.get('full-name')
            sender = request.POST.get('email')
            mobile = request.POST.get('phone-number')

            recipients = ['darshanbajania1999@gmail.com']
            subject = "Lakshmi Travels website Enquiry: Daily Trip/ Registered"
            message = "hello testing"
            message = "Name: "+name + "\nEmail Id: " + sender + "\nMobile No: " + \
                str(mobile) + "\n\nRoute: "+route + \
                "\nLocation: "+location + "\nDate: "+date
            send_mail(subject, message,
                      'darshanbajania1999@gmail.com', recipients)

        elif request.POST.get('item-category') == 'tour-package':

            destination = request.POST.get('destination')
            journey_start = request.POST.get('journey-start')
            journey_days = request.POST.get('days')
            adults = request.POST.get('adults')
            children = request.POST.get('children')
            tour_details = request.POST.get('tour-details')
            location = request.POST.get('location')
            date = request.POST.get('date')

            name = request.POST.get('full-name')
            sender = request.POST.get('email')
            mobile = request.POST.get('phone-number')

            recipients = ['darshanbajania1999@gmail.com']
            subject = "Lakshmi Travels website Enquiry: Tour Package / Registered"
            message = "hello testing"
            message = "Name: "+name + "\nEmail Id: " + sender + "\nMobile No: " + \
                str(mobile) + "\n\nDestination: "+destination + "\nJourney Start: "+journey_start + "\nJourney Days: "+journey_days + \
                "\nAdults: "+adults + "\nChildren: "+children + "\nCutomer Requirements: " + \
                tour_details + "\nLcation: "+location 
            send_mail(subject, message,
                      'darshanbajania1999@gmail.com', recipients)

        else:
            print("hello")
            location = request.POST.get('location')
            date_r = request.POST.get('date_r')
            date_d = request.POST.get('date_d')

            print(date_r, date_d)


            name = request.POST.get('full-name')
            sender = request.POST.get('email')
            mobile = request.POST.get('phone-number')


            recipients = ['darshanbajania1999@gmail.com']
            subject = "Lakshmi Travels website Enquiry: Rental Car"
            message = "hello testing"
            
            
            if request.POST.get('enquiry-category') == 'daily-trip':
                route = request.POST.get('route')
                subject = "Lakshmi Travels website Enquiry: Daily Trip/ Not Registered"

                message = "Name: "+name + "\nEmail Id: " + sender + "\nMobile No: " + \
                    str(mobile) + "\n\nRoute: "+route + \
                    "\nLocation: "+location + "\nDate: "+ date_d

                send_mail(subject, message,
                        'darshanbajania1999@gmail.com', recipients)
            
            elif request.POST.get('enquiry-category') == 'rental-car':
                car_model = request.POST.get('car_model')
                subject = "Lakshmi Travels website Enquiry: Rental Car/ Not Registered"

                message = "Name: "+name + "\nEmail Id: " + sender + "\nMobile No: " + \
                    str(mobile) + "\n\nCar Model: "+car_model + \
                    "\nLocation: "+location + "\nDate: "+date_r
                send_mail(subject, message,
                        'darshanbajania1999@gmail.com', recipients)
            elif request.POST.get('enquiry-category') == 'tour-package':

                destination = request.POST.get('destination')
                journey_start = request.POST.get('journey-start')
                journey_days = request.POST.get('days')
                adults = request.POST.get('adults')
                children = request.POST.get('children')
                tour_details = request.POST.get('tour-details')
                subject = "Lakshmi Travels website Enquiry: Tour Package/ Not registered"

                message = "Name: "+name + "\nEmail Id: " + sender + "\nMobile No: " + \
                    str(mobile) + "\n\nDestination:  " + "\nAdults: "+adults + "\nAdults: "+adults + destination + "\nJourney Start: "+journey_start + "\nJourney Days: "+journey_days + \
                    + "\nAdults: "+adults + "\nChildren: "+children + "\nCutomer Requirements: " + \
                    tour_details + "\nLocation: "+location
                send_mail(subject, message,
                            'darshanbajania1999@gmail.com', recipients)

    if booking_type == 'rental_car':
        selected_car = RentalCars.objects.all().filter(car_id=car_request_id).first()
        if selected_car != None:
            booking_type = 'rental_car'
    elif booking_type == 'daily_trip':

        selected_trip = TripDetails.objects.all().filter(id=daily_trip_id).first()

    elif booking_type == 'tour_package':
        selected_tour = TourPackageDetails.objects.all().filter(
            tour_id=tour_package_id).first()
        print(selected_tour)

    # print(booking_type, car_request_id, daily_trip_id)
    context = {
        'booking_type': booking_type,
        'selected_car': selected_car,
        'selected_trip': selected_trip,
        'selected_tour': selected_tour,
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

            user = authenticate(username=login_username,
                                password=login_password)
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
    all_tours = TourPackageDetails.objects.all()
    if request.method == "POST":
        change_type = request.POST.get('change_type')

        if change_type == 'add_new':
            return redirect('lakshmi_travels:admin_dashboard_tours_form')
        if change_type == 'delete_tour':
            tour_id = request.POST.get('delete_tour_id')
            print(tour_id)
            if tour_id is not None:
                sel_tour = TourPackageDetails.objects.all().filter(tour_id=tour_id).first()
                sel_tour.delete()

    context = {
        'all_tours': all_tours,
    }

    return render(request, 'lakshmi_travels/admin_dashboard_tours.html', context)


@login_required
def AdminDashBoardToursFormView(request):
    all_tours = TourPackageDetails.objects.all()
    # IST = pytz.timezone('Asia/Kolkata')
    # print(datetime.now(IST))
    if request.method == 'POST':
        tour_name = request.POST.get('tour_name')
        tour_summary = request.POST.get('tour_summary')
        tour_duration = request.POST.get('tour_duration')
        tour_image = request.FILES['tour_image']
        tour_details = request.POST.get('tour_details')

        print(tour_name, tour_summary, tour_duration, tour_image, tour_details)
        if tour_name is not None and tour_summary is not None and tour_duration is not None and tour_image is not None and tour_details is not None:
            latest_id = TourPackageDetails.objects.all().order_by(
                'tour_id').reverse().first().id
            print(latest_id)
            new_tour = TourPackageDetails(tour_id=latest_id + 1,
                                          package_name=tour_name,
                                          summary=tour_summary,
                                          duration=tour_duration,
                                          details=tour_details,
                                          tour_package_image=tour_image,
                                          availability_status=True)
            new_tour.save()

    td_form = TripDetailsForm()
    context = {
        'td_form': td_form,
        'all_tours': all_tours,
    }

    return render(request, 'lakshmi_travels/admin_dashboard_tours_form.html', context)


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
    all_daily_trips = TripDetails.objects.all()
    if request.method == "POST":
        change_type = request.POST.get('change_type')
        trip_id = request.POST.get('trip_price')

        if change_type == 'add_new':
            return redirect('lakshmi_travels:admin_dashboard_daily_trip_form')
        if change_type == 'delete_trip':
            trip_id = request.POST.get('delete_trip_id')
            print(trip_id)
            if trip_id is not None:
                sel_trip = TripDetails.objects.all().filter(trip_id=trip_id).first()
                sel_trip.delete()

    context = {
        'all_daily_trips': all_daily_trips,
    }

    return render(request, 'lakshmi_travels/admin_dashboard_daily_trips.html', context)


@login_required
def AdminDashBoardDailyTripsFormView(request):
    all_daily_trips = TripDetails.objects.all()
    IST = pytz.timezone('Asia/Kolkata')
    # print(datetime.now(IST))
    if request.method == 'POST':
        trip_route = request.POST.get('trip_route')
        trip_date = request.POST.get('trip_date')
        trip_price = request.POST.get('trip_price')
        # print(trip_date)
        trip_date = datetime.strptime(trip_date, "%Y-%m-%dT%H:%M")
        # print(trip_date)
        trip_date = timezone.make_aware(trip_date, timezone=IST)
        # print(trip_route, trip_price, trip_date)

        if trip_route is not None and trip_date is not None and trip_price is not None:
            latest_id = TripDetails.objects.all().order_by('trip_id').reverse().first().id
            # print(latest_id)
            new_trip = TripDetails(trip_id=latest_id + 1,
                                   route=trip_route, trip_timings=trip_date)
            new_trip.save()

    td_form = TripDetailsForm()
    context = {
        'td_form': td_form,
        'all_daily_trips': all_daily_trips,
    }

    return render(request, 'lakshmi_travels/admin_dashboard_daily_trip_form.html', context)
