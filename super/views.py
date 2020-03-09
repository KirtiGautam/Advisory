from Advisor import views
from Advisor.models import teachers, department, Users
from django.shortcuts import render, redirect
from django.http import JsonResponse


def getHods(request):
    if 'user' in request.session:
        hods = teachers.objects.raw('''SELECT * FROM advisor_teachers WHERE full_name LIKE "%%''' +
                                    request.POST['term'] + '''%%" AND department_id = ''' + request.POST['dept'])

        data = {
            "hods": [[hod.full_name, hod.id] for hod in hods]
        }
        return JsonResponse(data)


def updatedeps(request):
    if 'user' in request.session:
        dept = department.objects.create(name=request.POST['dept'])
        print(dept)
        data = {
            'success': True,
            'deptid': dept.id,
            'deptHOD': dept.HOD,
            'dept': dept.name,
        }
        return JsonResponse(data)


def updatehod(request):
    if 'user' in request.session:
        try:
            try:
                prev = teachers.objects.get(
                    full_name=request.POST['prev'])
                prev_user = Users.objects.get(uid=prev)
                prev_user.admin = False
                prev_user.save()
            except teachers.DoesNotExist:
                print('No such teacheer')

            next = teachers.objects.get(
                full_name=request.POST['name'])
            user = Users.objects.get(uid=next)
            user.admin = True
            user.save()
        except Users.DoesNotExist:
            print('No such User')
            user = Users.objects.create_admin(
                username=request.POST['name'], password=request.POST['name'], uid=teachers.objects.get(full_name=request.POST['name']))
        hod = department.objects.get(id=request.POST['dept'])
        hod.HOD = request.POST['name']
        hod.save()
        data = {
            'success': True,
        }
        return JsonResponse(data)


def editAdmins(request):
    if 'user' in request.session:
        teacher = teachers.objects.all()
        Hod = department.objects.all()
        context = {'teachers': teacher, 'hod': Hod,
                   'user': Users.objects.get(id=request.session['user'])}
        return render(request, 'Superuser\editAdmins.html', context)
    else:
        return redirect('Advisor:index')
