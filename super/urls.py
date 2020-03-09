from django.urls import path

from . import views

app_name = 'Super'

urlpatterns = [
    path(r'editAdmin', views.editAdmins, name='editAdmin'),
    path(r'get-hods', views.getHods, name='getH'),
    path(r'update-hod', views.updatehod, name='updateH'),
    path(r'update-deps', views.updatedeps, name='updateD'),
]
