from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    if 'user' in request.session:
        return render(request, 'Mentors/Students.html')
    else:
        return redirect('Advisor:dashboard')