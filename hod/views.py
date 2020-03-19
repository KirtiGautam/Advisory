from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission
from Advisor.models import Users, teachers, Class
from django.db.models import Q
from django.http import JsonResponse
from django.core import serializers


# Create your views here.


def createClass(request):
    if 'user' in request.session:
        clas, created = Class.objects.get_or_create(
            section=request.POST['section'], batch=request.POST['batch'])
        clas.Mentor = teachers.objects.get(id=request.POST['Mentor'])
        clas.save()
        data = {
            'success': True,
            'created': created,
            'Class': clas,
        }
        return JsonResponse(data)


def updateClass(request):
    if 'user' in request.session:
        clas = Class.objects.get(id=request.POST['id'])
        clas.Mentor = teachers.objects.get(id=request.POST['Mentor'])
        clas.save()
        c = [clas.section, str(clas.Mentor), clas.batch]
        data = {
            'success': True,
            'Class': c,
        }
        return JsonResponse(data)


def deleteClass(request):
    if 'user' in request.session:
        clas = Class.objects.get(id=request.POST['delete'])
        clas.delete()
        data = {
            'success': True,
            'Class': clas,
        }
        return JsonResponse(data)


def getTeachers(request):
    if 'user' in request.session:
        teacher = teachers.objects.raw('''SELECT * FROM advisor_teachers WHERE full_name LIKE "%%''' +
                                       request.POST['term'] + '''%%" AND department_id = ''' + str(request.user.teacher.department.id))
        data = {
            'teachers': [[teach.full_name, teach.id, teach.contact] for teach in teacher],
        }
        return JsonResponse(data)
    else:
        return redirect('Advisor:index')


def mentor(request):
    if 'user' in request.session:
        context = {
            'mentor': Class.objects.all()
        }
        return render(request, 'Admin/Mentor.html', context)
    else:
        return redirect('Advisor:index')


def role(request):
    if 'user' in request.session:
        perm = Permission.objects.get(codename='can_upload_students')
        useru = Users.objects.filter(
            Q(groups__permissions=perm) | Q(user_permissions=perm)).distinct().first()
        perm = Permission.objects.get(codename='can_assign_mentors')
        usera = Users.objects.filter(
            Q(groups__permissions=perm) | Q(user_permissions=perm)).distinct().first()
        context = {
            'can_upload': useru,
            'can_assign': usera,
        }
        return render(request, 'Admin/role.html', context)
    else:
        return redirect('Advisor:index')
