from django.contrib import admin
from .models import RentalCars, TripDetails, Customers, TourPackageDetails

# Register your models here.


admin.site.register(RentalCars)
admin.site.register(TripDetails)
admin.site.register(Customers)
admin.site.register(TourPackageDetails)