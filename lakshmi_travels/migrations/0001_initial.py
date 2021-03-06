# Generated by Django 3.2.5 on 2021-08-14 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RentalCars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_id', models.IntegerField(default='0')),
                ('model_name', models.CharField(default='car', max_length=200)),
                ('r_number', models.CharField(default='abc', max_length=100)),
                ('seating_capacity', models.IntegerField(default='4')),
                ('rate_per_day', models.IntegerField(default='2000')),
                ('km_per_day', models.IntegerField(default='10')),
                ('extra_km_per_day', models.IntegerField(default='15')),
                ('availabilty_status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='TripDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_id', models.IntegerField(default='0')),
                ('route', models.CharField(default='route1', max_length=400)),
                ('trip_timings', models.DateTimeField()),
                ('availability_status', models.BooleanField(default=True)),
            ],
        ),
    ]
