# dashboard/urls.py
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home_dashboard, name='home'),
    path('usuarios/', views.usuarios_table, name='usuarios_table'),
    path('publicaciones/', views.publicaciones_table, name='publicaciones_table'),
]
