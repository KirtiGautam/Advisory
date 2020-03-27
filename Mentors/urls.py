from django.urls import path

from Mentors import views

app_name = 'Mentor'

urlpatterns = [
    path(r'students', views.index, name='students'),
    path(r'get-students', views.getStudents, name='getstudents'),
]
