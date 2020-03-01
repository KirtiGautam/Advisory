from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'dashboard', views.dashboard, name='dashboard'),
    path(r'superuser',views.superuser,name='super'),
]