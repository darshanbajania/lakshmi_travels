from django.db import models
from django.contrib.auth.models import User
import datetime

from django.db.models.fields import CharField 


# Create your models here.

class RentalCars(models.Model):
    car_id = models.IntegerField(default='0', unique=True)
    model_name = models.CharField(default='car', max_length=200)
    car_image = models.ImageField(default="default_car.jpg", upload_to='rental_car_images')
    r_number = models.CharField(default='abc', max_length = 100)
    seating_capacity = models.CharField(default='4', max_length = 10)
    rate_per_day = models.CharField(default='2000', max_length = 10)
    km_allowed_per_day = models.CharField(default='10', max_length = 10)
    extra_km_per_day = models.CharField(default='15', max_length = 10)
    availabilty_status = models.BooleanField(default=True)


    def __str__(self):
        return f'{self.model_name}'

class TripDetails(models.Model):
    trip_id = models.IntegerField(default='0')
    route = models.CharField(default='route1', max_length=400)
    trip_timings = models.DateTimeField()
    availability_status = models.BooleanField(default=True)
 
    def __str__(self):
        return f'{self.route} ' + f'{self.trip_timings}'

# class Customers(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Profile')
#     customer_id = models.CharField(default="no_id", max_length=20)
#     full_name = models.CharField(default="user", max_length=100)
#     email_id = models.CharField(default="user.gmail.com", max_length=100)
#     address = models.CharField(default="address", max_length=500)
#     purchased_product_id = models.CharField(default="[]", max_length=500)
#     currently_purchased_products = models.CharField(default="{}", max_length=200)

#     def __str__(self):
#         return f'Customer:  {self.customer_id}'

#     def save(self, *args, **kwargs):
#         super().save()
