from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from Advisor.controllers import indexController, superuserController

# Create your views here.

def index(request):
    return indexController.index(request)

def dashboard(request):
    return indexController.dashboard(request)

def settings(request):
    if 'user' in request.session:
        return render(request, 'Master\settings.html')
    else:
        return redirect(index)

def editAdmins(request):
    return superuserController.editAdmins(request)

def logout(request):
    return indexController.log(request)