from django.urls import path

from Mentors import views

app_name = 'Mentor'

urlpatterns = [
    path(r'picture-upload', views.imageStu, name='StuImage'),
    path(r'students', views.index, name='students'),
    path(r'get-students', views.getStudents, name='getstudents'),
    path(r'get-student', views.getStudent, name='getstudent'),
    path(r'create-student', views.createStudent, name='cretestudent'),
    path(r'update-student', views.updateStudent, name='updateStudent'),
    path(r'update-sprof', views.updateSProf, name='updateSProf'),
    path(r'updated-sprof', views.updatedStu, name='updatedStu'),
    path(r'get-pin', views.getPin, name='getpin'),
]
