from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import views as auth_views



app_name = 'lakshmi_travels'


urlpatterns = [
    path('', views.Home, name='home_view'),
    path('tour_packages/', views.TourPackagesView, name='tour_packages'),
    path('daily_trip/', views.DailyTripView, name='daily_trip'),
    path('enquiry/', views.EnquiryPageview, name='enquiry_page'),
    path('tour_package_details/', views.TourPackageDetailsView, name='tour_package_details'),


    path('login/', views.LoginView, name='login_page'),
    path('logout/', LogoutView.as_view(next_page='lakshmi_travels:home_view'),name="logout_url"),
    path('register/', views.RegisterView, name='register_page'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),  name="password_change"),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name="password_change_done"),


    path('customer_dashboard/', views.CustomerDashboardView, name='customer_dashboard_page'),
    path('admin_dashboard/', views.AdminDashBoardView, name='admin_dashboard'),
    path('admin_dashboard/customers/', views.AdminDashBoardCustomersView, name='admin_dashboard_customers'),
    path('admin_dashboard/tours/', views.AdminDashBoardToursView, name='admin_dashboard_tours'),
    path('admin_dashboard/tours/modify', views.AdminDashBoardToursFormView, name='admin_dashboard_tours_form'),
    path('admin_dashboard/rental_cars/', views.AdminDashBoardRentalCarsView, name='admin_dashboard_rental_cars'),
    path('admin_dashboard/daily_trips/', views.AdminDashBoardDailyTripsView, name='admin_dashboard_daily_trips'),
    path('admin_dashboard/daily_trips/modify', views.AdminDashBoardDailyTripsFormView, name='admin_dashboard_daily_trip_form'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
