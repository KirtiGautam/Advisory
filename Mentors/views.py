from django.shortcuts import render, redirect
from Advisor.models import students, Class
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers


# Create your views here.


def index(request):
    if 'user' in request.session:
        return render(request, 'Mentors/Students.html')
    else:
        return redirect('Advisor:dashboard')


def createStudent(request):
    if 'user' in request.session:
        student = students.objects.Create(
            urn=request.POST['urn'],
            crn=request.POST['crn'],
            full_name=request.POST['full_name'],
            gender=request.POST['gender'],
            blood_group=request.POST['blood_type'],
            category=request.POST['category'],
            height=request.POST['height'],
            weight=request.POST['weight'],
            living=request.POST['living'],
            Father_name=request.POST['Father_name'],
            Father_contact=request.POST['Father_contact'],
            Mother_name=request.POST['Mother_name'],
            Mother_contact=request.POST['Mother_contact'],
            Address=request.POST['Address'],
            City=request.POST['City'],
            State=request.POST['State'],
            District=request.POST['District'],
            Pincode=request.POST['Pincode'],
            Contact=request.POST['Contact'],
            email=request.POST['email'],
            Class=Class.objects.get(name=request.POST['Class']),)


def deleteStudent(request):
    if 'user' in request.session:
        student = students.objects.get(id=request.POST['student'])
        student.delete()
        data = {
            'success': True,
            'student': student,
        }
        return JsonResponse(data)


def getStudent(request):
    if 'user' in request.session:
        student = students.objects.get(urn=request.POST['student'])
        rec = serializers.serialize(
            'json', [student], indent=2, use_natural_foreign_keys=True)
        data = {
            'success': True,
            'student': rec,
        }
        return JsonResponse(data)


def getStudents(request):
    if 'user' in request.session:
        Clas = Class.objects.get(Mentor=request.user.teacher)
        student = students.objects.raw('''SELECT * FROM advisor_students WHERE (full_name LIKE "%%''' +
                                       request.POST['term'] + '''%%"OR urn LIKE "%%''' +
                                       request.POST['term'] + '''%%") AND Class_id = ''' + str(Clas.id))
        rec = serializers.serialize(
            'json', student, indent=2, use_natural_foreign_keys=True)
        data = {
            'success': True,
            'student': rec,
        }
        return JsonResponse(data)
