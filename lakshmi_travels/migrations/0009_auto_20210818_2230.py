# Generated by Django 3.2.5 on 2021-08-18 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lakshmi_travels', '0008_tourpackagedetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourpackagedetails',
            name='tour_package',
            field=models.ImageField(default='tour_package.jpg', upload_to='tour_package_images'),
        ),
        migrations.AlterField(
            model_name='tourpackagedetails',
            name='duration',
            field=models.CharField(default='1 Week', max_length=100),
        ),
    ]