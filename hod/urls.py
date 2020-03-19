from django.urls import path

from . import views

app_name = 'Admin'

urlpatterns = [
    path(r'role', views.role, name='role'),
    path(r'mentor', views.mentor, name='mentor'),
    path(r'update-class', views.updateClass, name='updateClass'),
    path(r'get-teachers', views.getTeachers, name='getTeachers')
]