from Advisor import views
from Advisor.models import teachers, department, Users
from django.shortcuts import render, redirect
from django.http import JsonResponse


def deletedep(request):
    if 'user' in request.session:
        dep = department.objects.get(id=request.POST['delete'])
        dep.delete()
        d={'id':dep.id, 'HOD': dep.HOD, 'name': dep.name}
        data = {
            'success': True,
            'dep': d,
        }
        return JsonResponse(data)


def updatedeps(request):
    if 'user' in request.session:
        dept, created = department.objects.get_or_create(
            name=request.POST['dept'].lower())

        data = {
            'success': True,
            'created': created,
            'deptid': dept.id,
            'deptHOD': dept.HOD,
            'dept': dept.name.title(),
        }
        return JsonResponse(data)


def updatehod(request):
    if 'user' in request.session:
        try:
            try:
                prev = teachers.objects.get(
                    full_name=request.POST['prev'])
                prev_user = Users.objects.get(teacher=prev)
                prev_user.admin = False
                prev_user.save()
            except teachers.DoesNotExist:
                print('No such teacheer')
            next = teachers.objects.get(
                id=request.POST['id'])
            user = Users.objects.get(teacher=next)
            user.admin = True
            user.save()
        except Users.DoesNotExist:
            print('No such User')
            user = Users.objects.create_admin(
                username=next.full_name, password=next.full_name, teacher=next)
        hod = department.objects.get(id=request.POST['dept'])
        hod.HOD = next.full_name
        hod.save()
        data = {
            'success': True,
            'hod': next.full_name
        }
        return JsonResponse(data)


def getHods(request):
    if 'user' in request.session:
        teacher = teachers.objects.raw('''SELECT * FROM advisor_teachers WHERE full_name LIKE "%%''' +
                                       request.POST['term'] + '''%%" AND department_id = ''' + request.POST['dept'])

        data = {
            "teachers": [[teach.full_name, teach.id, teach.contact] for teach in teacher]
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
