from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from Advisor.controllers import indexController

# Create your views here.

def index(request):
    return indexController.index(request)

def dashboard(request):
    return indexController.dashboard(request)

def settings(request):
    return render(request, 'Master\settings.html')

def editAdmins(request):
    return render(request, 'Superuser\editAdmins.html')

def logout(request):
    return indexController.log(request)