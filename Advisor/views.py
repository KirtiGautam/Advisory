from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from Advisor.models import Users, teachers, department, Class, students, detailed_Marks, Subjects
from django.http import JsonResponse
from django.core import serializers
import json
import os
from PIL import Image
from datetime import datetime, date
import random
import string
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


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
                if user.first_login and not user.is_superuser:
                    teacher = teachers.objects.values('full_name').get(
                        EID=user.teacher.EID)
                    print(teacher)
                    return render(request, 'Master/firstlogin.html', {'username': request.POST['username'], 'name': teacher['full_name']})
                else:
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


def firstlogin(request):
    if request.method == 'POST':
        user = Users.objects.get(username=request.POST['username'])
        user.set_password(request.POST['password'])
        user.first_login = False
        user.save()
        login(request, user)
        request.session['user'] = str(user.id)
        return redirect('Advisor:dashboard')
    else:
        return redirect('Advisor:index')


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
                t = []
                for d in dat:
                    dep = department.objects.get(
                        name=d.pop('department').lower())
                    t.append(teachers(department=dep, **d))
                teachers.objects.bulk_create(t)
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
            elif model == 'department':
                deps = []
                for d in dat:
                    name = d.pop('name')
                    if name != '':
                        deps.append(department(name=name.lower()))
                department.objects.bulk_create(deps)
            elif model == 'subject':
                subs = []
                for d in dat:    
                    if request.user.is_superuser:
                        subs.append(Subjects(department=department.objects.get(name=d.pop('name')), **d))
                    else:                    
                        subs.append(Subjects(department=request.user.teacher.department, **d))                
                Subjects.objects.bulk_create(subs)
            elif model == 'Class':
                mentors = []
                emails = []
                from_email = 'E-Advisory Systems'
                subject = 'Credentials for E-Advisory'
                for d in dat:
                    teacher = teachers.objects.get(EID=d.pop('MentorEID'))
                    user, created = Users.objects.get_or_create(
                        username=teacher.EID, teacher=teacher)
                    if created:
                        password_characters = string.ascii_letters + string.digits + string.punctuation
                        password = ''.join(random.choice(password_characters)
                                           for i in range(random.randint(8, 12)))
                        user.set_password(password)
                        conx = {'host': request.get_host(),
                                'username': teacher.EID, 'password': password}
                        html_message = render_to_string(
                            'Mails/usercreatemail.html', conx)
                        plain_message = strip_tags(html_message)
                        emails.append((subject, plain_message, from_email, [teacher.email]))
                    user.save()
                    mentors.append(
                        Class(Mentor=teacher, department=request.user.teacher.department, **d))
                Class.objects.bulk_create(mentors)
                mail.send_mass_mail((message for message in emails))
            else:
                s = []
                for d in dat:
                    clas = Class.objects.get(section=d.pop(
                        'section'), batch=d.pop('batch'), department=request.user.teacher.department)
                    cr_date = datetime.strptime(
                        d.pop('dob'), '%d-%m-%Y')
                    do = cr_date.strftime('%Y-%m-%d')
                    s.append(students(dob=do, Class=clas, **d))
                students.objects.bulk_create(s)
            data = {
                'success': True,
            }
            return JsonResponse(data)
        else:
            return render(request, 'Master/data.html')
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
