from django.urls import path
from . import views

app_name = 'relacion'

urlpatterns = [
    # API REST
    path('api/seguidor/', views.SeguidorCreateView.as_view(), name='api-seguidor-list-create'),
    path('api/seguidor/<int:pk>/', views.SeguidorDetailView.as_view(), name='api-seguidor-detail'),

    # Vistas que usan templates
    path('lista/', views.lista_relaciones, name='lista-relaciones'),
    path('detalle/<int:pk>/', views.detalle_relacion, name='detalle-relacion'),
]
