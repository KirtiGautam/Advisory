from django.urls import path

from Advisor import views

app_name = 'Advisor'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'dashboard', views.dashboard, name='dashboard'),
    path(r'settings', views.settings, name='settings'),
    path(r'logout', views.log, name='logout'),
    path(r'change-password', views.changePass, name='changeP'),
    path(r'upload-data', views.uploadData, name='uploadData'),
    path(r'user-pic', views.UserPic, name='UserPic'),
]
