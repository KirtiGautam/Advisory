from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'dashboard', views.dashboard, name='dashboard'),
    path(r'settings', views.settings, name='settings'),
    path(r'editAdmin', views.editAdmins, name='editAdmin'),
    path(r'logout', views.logout, name='logout')

]
