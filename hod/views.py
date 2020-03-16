from django.shortcuts import render, redirect

# Create your views here.


def mentor(request):
    if 'user' in request.session:
        return render(request, 'Admin/Mentor.html')
    else:
        return redirect('Advisor:index')


def role(request):
    if 'user' in request.session:
        return render(request, 'Admin/role.html')
    else:
        return redirect(request, 'Advisor:index')
