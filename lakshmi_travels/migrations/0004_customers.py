# Generated by Django 3.2.5 on 2021-08-17 08:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lakshmi_travels', '0003_rentalcars_car_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(default='no_id', max_length=20)),
                ('full_name', models.CharField(default='user', max_length=100)),
                ('email_id', models.CharField(default='user.gmail.com', max_length=100)),
                ('address', models.CharField(default='address', max_length=500)),
                ('purchased_product_id', models.CharField(default='[]', max_length=500)),
                ('currently_purchased_products', models.CharField(default='{}', max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
