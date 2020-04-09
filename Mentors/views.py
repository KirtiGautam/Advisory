from django.shortcuts import render, redirect
from Advisor.models import students, Class, marks
from django.http import JsonResponse, FileResponse, HttpResponse
from django.core import serializers
import os
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
        }
        return JsonResponse(data)


def updatedStu(request):
    if 'user' in request.session:
        if request.method == 'POST':
            values = {k: v for k, v in request.POST.items()}
            values.pop('csrfmiddlewaretoken')
            student = students.objects.filter(
                urn=values.pop('urn')).update(**values)
            return redirect('Mentor:students')


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


def updateSProf(request):
    if 'user' in request.session:
        if request.method == 'POST':
            return render(request, 'Mentors/updateStu.html', {'student': students.objects.get(urn=request.POST['student'])})


def updateStudent(request):
    student = students.objects.get(urn=request.POST['urn'])
    if student.Father_pic:
        os.remove('Media/'+student.Father_pic.name)
    if student.Mother_pic:
        os.remove('Media/'+student.Mother_pic.name)
    if student.photo:
        os.remove('Media/'+student.photo.name)
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
