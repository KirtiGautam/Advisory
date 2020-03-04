from Advisor import views
from Advisor.models import teachers, department
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers


def editAdmins(request):
    if 'user' in request.session:
        teacher = teachers.objects.all()
        Hod = department.objects.all()
        context = {'teachers': teacher, 'hod': Hod}
        return render(request, 'Superuser\editAdmins.html', context)
    else:
        return redirect(views.index)


def hods(request):
    if 'user' in request.session:
        # raw('''SELECT * FROM advisor_teachers WHERE full_name LIKE "%%''' +
        #                             request.POST['term'] + '''%%" AND department_id = ''' + request.POST['dept'])
        data = {
            "hods": [hod for hod in teachers.objects.filter(department=request.POST['dept']).values()]
        }
        return JsonResponse(data)
