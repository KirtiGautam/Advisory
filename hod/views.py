from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission
from Advisor.models import Users, teachers, Class, department, Subjects
from django.db.models import Q
from django.http import JsonResponse
from django.db import IntegrityError

# Create your views here.


def deleteSubject(request):
    if 'user' in request.session:
        print(request.POST['id'])
        subject = Subjects.objects.get(sub_code=request.POST['id'])
        subject.delete()
        data = {
            'success': True,
        }
        return JsonResponse(data)

    else:
        return redirect('Advisor:index')


def addSubject(request):
    if 'user' in request.session:
        values = {k: v for k, v in request.POST.items()}
        try:
            subject, created = Subjects.objects.get_or_create(department=department.objects.get(
                id=values.pop('department')), **values)
            data = {
                'success': True,
                'superuser': request.user.is_superuser,
            }
            if request.user.is_superuser:
                data['department'] = str(subject.department).title()
        except IntegrityError:
            data = {
                'success': False,
                'message': 'Already exists',
            }
        return JsonResponse(data)
    else:
        return redirect('Advisor:index')


def subjects(request):
    if 'user' in request.session:
        if request.user.is_superuser:
            subjects = Subjects.objects.all()
            departments = department.objects.all()
            context = {
                'subjects': subjects,
                'departments': departments,
            }
        elif request.user.admin:
            subjects = Subjects.objects.filter(
                department=request.user.teacher.department)
            context = {
                'subjects': subjects,
            }
        else:
            return redirect('Advisor:dashboard')
        return render(request, 'Admin/subjects.html', context)
    else:
        return redirect('Advisor:index')


def createClass(request):
    if 'user' in request.session:
        teach = teachers.objects.get(id=request.POST['Mentor'])
        clas, Ccreated = Class.objects.get_or_create(
            section=request.POST['section'], batch=request.POST['batch'], department=request.user.teacher.department, Mentor=teach)
        obj, created = Users.objects.get_or_create(
            username=teach.full_name, teacher=teach)
        if not created:
            obj.set_password(teach.full_name)
            obj.save()
        c = {'id': clas.id, 'section': clas.section,
             'Mentor': str(clas.Mentor), 'batch': clas.batch}
        data = {
            'success': True,
            'created': Ccreated,
            'Class': c,
        }
        return JsonResponse(data)


def updateClass(request):
    if 'user' in request.session:
        clas = Class.objects.get(id=request.POST['id'])
        if request.user.teacher.department.id != request.POST['department']:
            clas.department = department.objects.get(
                id=request.POST['department'])
        try:
            prev = Users.objects.get(teacher=clas.Mentor)
            prev.delete()
        except Users.DoesNotExist:
            print('User Does not exist')
        teach = teachers.objects.get(id=request.POST['Mentor'])
        clas.Mentor = teach
        clas.save()
        obj, created = Users.objects.get_or_create(
            username=teach.full_name, teacher=teach)
        if created:
            obj.set_password(teach.full_name)
            obj.save()
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
        depart = request.user.teacher.department
        context = {
            'mentor': Class.objects.filter(department=depart),
            'departments': department.objects.all(),
        }
        return render(request, 'Admin/Mentor.html', context)
    else:
        return redirect('Advisor:index')


def role(request):
    if 'user' in request.session:
        perm = Permission.objects.get(codename='can_upload_students')
        useru = Users.objects.filter(
            Q(groups__permissions=perm) | Q(user_permissions=perm)).filter(teacher__department=request.user.teacher.department).distinct().first()
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


def updatePerms(request):
    if 'user' in request.session:
        teacher = teachers.objects.get(id=request.POST['teach'])
        user, created = Users.objects.get_or_create(
            username=teacher.full_name, teacher=teacher)
        if created:
            user.set_password(teacher.full_name)
            user.save()
        perm = Permission.objects.get(codename=request.POST['permission'])
        prev_user = Users.objects.filter(
            user_permissions=perm, teacher__department=request.user.teacher.department)
        for u in prev_user:
            u.user_permissions.remove(perm)
            u.save()
        user.user_permissions.add(perm)
        user.save()
        data = {
            'success': True,
            'user': user.teacher.full_name,
        }
        return JsonResponse(data)
