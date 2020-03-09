from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from Advisor.models import Users, teachers, department
from django.http import JsonResponse
import json

# Create your views here.


def index(request):
    if 'user' in request.session:
        return redirect('Advisor:dashboard')
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
            return redirect('Advisor:index')
    else:
        if 'user' in request.session:
            context = {'user': Users.objects.get(
                id=request.session['user'])}
            return render(request, 'Master/dashboard.html', context)
        else:
            return redirect('Advisor:index')


def log(request):
    logout(request)
    return redirect('Advisor:index')


def settings(request):
    if 'user' in request.session:
        context = {'user': Users.objects.get(id=request.session['user'])}
        return render(request, 'Master\settings.html', context)
    else:
        return redirect('Advisor:index')


def uploadtData(request):
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


def uploadData(request):
    if 'user' in request.session:
        context = {'user': Users.objects.get(id=request.session['user'])}
        return render(request, 'Master/data.html', context)
    else:
        return redirect('Advisor:index')


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
        return redirect(settings)
