from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.views import LoginView,LogoutView



app_name = 'lakshmi_travels'


urlpatterns = [
    path('', views.Home, name='home_view'),
    path('tour_packages/', views.TourPackagesView, name='tour_packages'),
    path('daily_trip/', views.DailyTripView, name='daily_trip'),
    path('enquiry/', views.EnquiryPageview, name='enquiry_page'),
    path('login/', views.LoginView, name='login_page'),
    path('logout/', LogoutView.as_view(next_page='lakshmi_travels:home_view'),name="logout_url"),
    path('register/', views.RegisterView, name='register_page'),
    path('customer_dashboard/', views.CustomerDashboardView, name='customer_dashboard_page'),
    path('admin_dashboard/', views.AdminDashBoardView, name='admin_dashboard'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
