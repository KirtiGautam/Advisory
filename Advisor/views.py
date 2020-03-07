from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from Advisor.models import Users
from Advisor.controllers import indexController, superuserController
from django.http import JsonResponse

# Create your views here.

def uploadtData(request):
    return indexController.tdata(request)

def uploadData(request):
    if 'user' in request.session:
        context = {'user': Users.objects.get(id=request.session['user'])}
        return render(request, 'Master\data.html', context)
    else:
        return redirect(index)

def updatedeps(request):
    return superuserController.updateDeps(request)

def updatehod(request):
    return superuserController.updateHod(request)


def getHods(request):
    return superuserController.hods(request)


def index(request):
    return indexController.index(request)


def dashboard(request):
    return indexController.dashboard(request)


def settings(request):
    if 'user' in request.session:
        context = {'user': Users.objects.get(id=request.session['user'])}
        return render(request, 'Master\settings.html', context)
    else:
        return redirect(index)


def editAdmins(request):
    return superuserController.editAdmins(request)


def logout(request):
    return indexController.log(request)


def changePass(request):
    if request.method == 'POST':
        use = Users.objects.get(id=request.session['user'])
        if use.check_password(request.POST['pre']):
            use.set_password(request.POST['password'])
            use.save()
            data = {
                'Changed': True
            }
        else:
            data = {
                'Changed': False
            }
        return JsonResponse(data)
    else:
        return render(settings)
