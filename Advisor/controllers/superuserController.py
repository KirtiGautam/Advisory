from Advisor import views
from Advisor.models import teachers, department
from django.shortcuts import render, redirect

def editAdmins(request):
    if 'user' in request.session:
        teacher = teachers.objects.all()
        Hod = department.objects.all()
        context={'teachers': teacher, 'hod': Hod}
        return render(request, 'Superuser\editAdmins.html', context)
    else:
        return redirect(index)