from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from Advisor.controllers import indexController

# Create your views here.

def index(request):
    return indexController.index(request)

def dashboard(request):
    return indexController.dashboard(request)

def superuser(request):
    return render(request, 'superuser_navbar.html')