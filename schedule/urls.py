from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stats/', views.stats, name='stats'),
    path('schedule/groups/', views.groups, name='groups'),
    path('schedule/groups/<int:pk>', views.group, name='group'),
    path('homework/', views.homework, name='homework'),
    path('homework/delete/<int:pk>', views.delete_homework, name='delete_homework'),
]
