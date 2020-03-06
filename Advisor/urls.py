from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'dashboard', views.dashboard, name='dashboard'),
    path(r'settings', views.settings, name='settings'),
    path(r'editAdmin', views.editAdmins, name='editAdmin'),
    path(r'logout', views.logout, name='logout'),
    path(r'change-password', views.changePass, name='changeP'),
    path(r'get-hods', views.getHods, name='getH'),
    path(r'update-hod', views.updatehod, name='updateH'),
    path(r'update-deps', views.updatedeps, name='updateD'),
]
