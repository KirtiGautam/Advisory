from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from Advisor.models import Users, teachers, department, Class, students
from django.http import JsonResponse
from django.core import serializers
import json
import os
from PIL import Image
from datetime import datetime, date


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
        model = request.POST['model']
        if model == 'teachers':
            for d in dat:
                dep = department.objects.get(name=d.pop('department').lower())
                t = teachers(department=dep, **d)
                t.save()
        else:
            for d in dat:
                clas = Class.objects.get(section=d.pop(
                    'section'), batch=d.pop('batch'))
                cr_date = datetime.strptime(
                    d.pop('dob'), '%d-%m-%Y')
                do = cr_date.strftime('%Y-%m-%d')
                s = students(dob=do, Class=clas, **d)
                s.save()
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


def UserPic(request):
    user = request.user
    if user.avatar:
        os.remove('Media/'+user.avatar.name)
    user.avatar = request.FILES['avatar']
    user.avatar.name = str(request.user.id)+'.jpg'
    user.save()
    rec = serializers.serialize(
        'json', [user], indent=2, use_natural_foreign_keys=True)
    data = {
        'success': True,
        'student': rec,
    }
    return JsonResponse(data)
