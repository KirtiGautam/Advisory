from Advisor import views
from Advisor.models import teachers, department, Users
from django.shortcuts import render, redirect
from django.http import JsonResponse
import random
import string
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def deletedep(request):
    if 'user' in request.session:
        dep = department.objects.get(id=request.POST['delete'])
        dep.delete()
        d = {'id': dep.id, 'HOD': dep.HOD, 'name': dep.name}
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
        prev_user = Users.objects.filter(teacher__department=request.POST['dept'], admin=True)
        if len(prev_user) > 0:
            prev_user = prev_user[0]
            prev_user.admin = False
            prev_user.save()
        next = teachers.objects.get(
            EID=request.POST['id'])
        user, created = Users.objects.get_or_create(
            username=next.EID, teacher=next)
        if created:
            password_characters = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(random.choice(password_characters)
                               for i in range(random.randint(8, 12)))
            subject = 'Credentials for E-Advisory'
            conx = {'host': request.get_host(),
                    'username': next.EID, 'password': password}
            html_message = render_to_string(
                'Mails/usercreatemail.html', conx)
            plain_message = strip_tags(html_message)
            from_email = 'E-Advisory Systems'
            # mail.send_mail(subject, plain_message, from_email, [
            #                next.email], html_message=html_message)
            user.set_password(password)
        user.admin = True
        user.save()
        hod = department.objects.get(id=request.POST['dept'])
        hod.HOD = next.full_name
        hod.save()
        data = {
            'success': True,
            'hod': next.full_name,
        }
        if created:
            data['username'] = next.EID
            data['password'] = password
        return JsonResponse(data)


def getHods(request):
    if 'user' in request.session:
        teacher = teachers.objects.filter(full_name__contains=request.POST['term'], department=request.POST['dept']).order_by(
            'full_name').values('full_name', 'EID', 'contact')
        data = {
            "teachers": list(teacher)
        }
        return JsonResponse(data)


def editAdmins(request):
    if 'user' in request.session:
        Hod = department.objects.all()
        context = {'hod': Hod}
        return render(request, 'Superuser\editAdmins.html', context)
    else:
        return redirect('Advisor:index')
