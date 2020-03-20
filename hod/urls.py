from django.urls import path

from . import views

app_name = 'Admin'

urlpatterns = [
    path(r'role', views.role, name='role'),
    path(r'mentor', views.mentor, name='mentor'),
    path(r'update-class', views.updateClass, name='updateClass'),
    path(r'create-class', views.createClass, name='createClass'),
    path(r'delete-class', views.deleteClass, name='deleteClass'),
    path(r'get-teachers', views.getTeachers, name='getTeachers'),
]