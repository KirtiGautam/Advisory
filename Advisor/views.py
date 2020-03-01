from django.shortcuts import render, redirect
from django.contrib.auth import authenticate

# Create your views here.


def index(request):
    if 'user' in request.session:
        return redirect(dashboard)
    else:
        return render(request, 'login.html')


def dashboard(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password'])
        if user is not None:
            request.session['user'] = str(user.uid)
            return render(request, 'dashboard.html', {'username': user.uid})
        else:
            return redirect(index)
    elif 'user' in request.session:
        return render(request, 'dashboard.html', {'username': request.session['user']})
    else:
        return redirect(index)

def superuser(request):
    return render(request, 'superuser_navbar.html')