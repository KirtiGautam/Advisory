from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from Advisor import views
from Advisor.models import Users


def index(request):
    if 'user' in request.session:
        return redirect(views.dashboard)
    else:
        return render(request, 'Master/login.html')


def dashboard(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password'])
        if user is not None:
            login(request, user)
            request.session['user'] = str(user.id)
            context = dict()
            context['username'] = user.uid
            return render(request, 'Master/dashboard.html', context)
        else:
            return redirect(views.index)
    elif 'user' in request.session:
        user = Users.objects.get(id = request.session['user'])
        context = dict()
        context['username'] = user.uid
        return render(request, 'Master/dashboard.html', context)
    else:
        return redirect(views.index)

def log(request):
    logout(request)
    return redirect(views.index)
