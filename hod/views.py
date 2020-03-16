from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission
from Advisor.models import Users, teachers
from django.db.models import Q
from django.http import JsonResponse

# Create your views here.

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
        return render(request, 'Admin/Mentor.html')
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
