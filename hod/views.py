from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission
from Advisor.models import Users, teachers, Class, department
from django.db.models import Q
from django.http import JsonResponse
from django.core import serializers


# Create your views here.


def createClass(request):
    if 'user' in request.session:
        teach = teachers.objects.get(id=request.POST['Mentor'])
        clas, created = Class.objects.get_or_create(
            section=request.POST['section'], batch=request.POST['batch'], department=request.user.teacher.department, Mentor=teach)
        Users.objects.create_user(
            username=teach.full_name, password=teach.full_name, teacher=teach)
        c = {'id': clas.id, 'section': clas.section,
             'Mentor': str(clas.Mentor), 'batch': clas.batch}
        data = {
            'success': True,
            'created': created,
            'Class': c,
        }
        return JsonResponse(data)


def updateClass(request):
    if 'user' in request.session:
        clas = Class.objects.get(id=request.POST['id'])
        try:
            prev = Users.objects.get(teacher=clas.Mentor)
            prev.delete()
        except Users.DoesNotExist:
            print('User Does not exist')
        teach = teachers.objects.get(id=request.POST['Mentor'])
        clas.Mentor = teach
        clas.save()
        Users.objects.create_user(
            username=teach.full_name, password=teach.full_name, teacher=teach)
        c = {'id': clas.id, 'section': clas.section,
             'Mentor': str(clas.Mentor), 'batch': clas.batch}
        data = {
            'success': True,
            'Class': c,
        }
        return JsonResponse(data)


def deleteClass(request):
    if 'user' in request.session:
        clas = Class.objects.get(id=request.POST['delete'])
        clas.delete()
        c = {'id': clas.id, 'section': clas.section,
             'Mentor': str(clas.Mentor), 'batch': clas.batch}
        data = {
            'success': True,
            'Class': c,
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
        depart= request.user.teacher.department
        context = {
            'mentor': Class.objects.filter(department=depart)
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
