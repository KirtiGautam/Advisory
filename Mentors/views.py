from django.shortcuts import render, redirect
from Advisor.models import students, Class, marks
from django.http import JsonResponse, FileResponse, HttpResponse
from django.core import serializers
from PIL import Image
import json


# Create your views here.

def imageStu(request):
    return render(request, 'Mentors/uploadImage.html')


def index(request):
    if 'user' in request.session:
        return render(request, 'Mentors/Students.html')
    else:
        return redirect('Advisor:dashboard')


def createStudent(request):
    if 'user' in request.session:
        dat = json.loads(request.POST['student'])
        clas = Class.objects.get(Mentor=request.user.teacher)
        s = students(Class=clas, **dat)
        s.save()
        data = {
            'success': True,
            'student': s,
        }
        return JsonResponse(data)


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
    try:
        student = students.objects.get(urn=request.POST['student'])
    except students.DoesNotExist:
        data = {
            'success': False,
            'message': 'No such User',
        }
        return JsonResponse(data)
    mark = marks.objects.filter(student=student)
    rec = serializers.serialize(
        'json', [student, student.Class, student.Class.department], indent=2, use_natural_foreign_keys=True)
    data = {
        'success': True,
        'student': rec,
        'marks': serializers.serialize(
            'json', mark, indent=2, use_natural_foreign_keys=True),
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


def updateStudent(request):
    student = students.objects.get(urn=request.POST['urn'])
    student.Father_pic = request.FILES['Father_pic']
    student.Mother_pic = request.FILES['Mother_pic']
    student.photo = request.FILES['photo']
    student.Father_pic.name = str(student.urn)+'.jpg'
    student.Mother_pic.name = str(student.urn)+'.jpg'
    student.photo.name = str(student.urn)+'.jpg'
    student.save()

    rec = serializers.serialize(
        'json', [student], indent=2, use_natural_foreign_keys=True)
    data = {
        'success': True,
        'student': rec,
    }
    return JsonResponse(data)
