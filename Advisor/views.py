from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from Advisor.models import Users, teachers, department, Class, students, detailed_Marks, Subjects
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
        if request.method == 'POST':
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password'])
            if user is not None:
                login(request, user)
                request.session['user'] = str(user.id)
                return redirect('Advisor:dashboard')
            else:
                context = {
                    'failed': True,
                }
                return render(request, 'Master/login.html', context)
        else:
            context = {
                'failed': False,
            }
            return render(request, 'Master/login.html', context)


def dashboard(request):
    if 'user' in request.session:
        return render(request, 'Master/dashboard.html')
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


def uploadData(request):
    if 'user' in request.session:
        if request.method == 'POST':
            dat = json.loads(request.POST['tdata'])
            model = request.POST['model']
            if model == 'teachers':
                for d in dat:
                    dep = department.objects.get(
                        name=d.pop('department').lower())
                    t = teachers(department=dep, **d)
                    t.save()
            elif model == 'marks':
                for d in dat:
                    urn = d.pop('urn')
                    cr_date = datetime.strptime(
                        d.pop('exam_date'), '%d-%m-%Y')
                    exD = cr_date.strftime('%Y-%m-%d')
                    dm, created = detailed_Marks.objects.get_or_create(subject=Subjects.objects.get(sub_code=d.pop('subject')), student=students.objects.get(
                        urn=urn), semester=d['semester'])
                    if created:
                        dm.exam_date = exD
                        dm.Sgpa = d['Sgpa']
                    else:
                        if dm.exam_date < datetime.date(cr_date):
                            dm.exam_date = exD
                            dm.Sgpa = d['Sgpa']
                            if dm.Sgpa != 0:
                                dm.passive_back = True
                    dm.save()
            else:
                for d in dat:
                    clas = Class.objects.get(section=d.pop(
                        'section'), batch=d.pop('batch'), department=request.user.teacher.department)
                    cr_date = datetime.strptime(
                        d.pop('dob'), '%d-%m-%Y')
                    do = cr_date.strftime('%Y-%m-%d')
                    s = students(dob=do, Class=clas, **d)
                    s.save()
            data = {
                'success': True,
            }
            return JsonResponse(data)
        else:
            context = {'user': Users.objects.get(id=request.session['user'])}
            return render(request, 'Master/data.html', context)
    else:
        return redirect('Advisor:index')


def changePass(request):
    if request.method == 'POST':
        use = request.user
        if use.check_password(request.POST['pre']):
            use.set_password(request.POST['password'])
            use.save()
            update_session_auth_hash(request, use)
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
        'user': rec,
    }
    return JsonResponse(data)
