from django.http import request
from django.shortcuts import render, redirect

# Create your views here.


def Home(request):
    return render(request, 'lakshmi_travels/index.html')