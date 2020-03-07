from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from Advisor import views
from Advisor.models import Users, teachers, department
from django.http import JsonResponse
import json


def tdata(request):
    if 'user' in request.session:
        dat = json.loads(request.POST['tdata'])
        for d in dat:
            teachers.objects.create(full_name=d['full_name'],
                                    gender=d['gender'],
                                    email=d['email'],
                                    contact=d['contact'],
                                    department=department.objects.get(id=d['department']),)
        data = {
            'success': True,
        }
        return JsonResponse(data)


def index(request):
    if 'user' in request.session:
        return redirect(views.dashboard)
    else:
        return render(request, 'Master/login.html')


def dashboard(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password'])
        if user is not None:
            login(request, user)
            request.session['user'] = str(user.id)
            context = {'user': user}
            return render(request, 'Master/dashboard.html', context)
        else:
            return redirect(views.index)
    else:
        if 'user' in request.session:
            context = {'user': Users.objects.get(
                id=request.session['user'])}
            return render(request, 'Master/dashboard.html', context)
        else:
            return redirect(views.index)


def log(request):
    logout(request)
    return redirect(views.index)
