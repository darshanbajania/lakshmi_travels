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

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
