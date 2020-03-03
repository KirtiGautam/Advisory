from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from Advisor.models import Users
from Advisor.controllers import indexController, superuserController
from django.http import JsonResponse

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


def changePass(request):
    if request.method == 'POST':
        use = Users.objects.get(id=request.session['user'])
        use.set_password(request.POST['password'])
        use.save()
        data = {
            'Changed': True
        }
        return JsonResponse(data)
    else:
        return render(settings)
