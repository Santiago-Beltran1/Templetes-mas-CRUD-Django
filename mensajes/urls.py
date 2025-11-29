from django.urls import path
from mensajes import views
from .views import MensajeCreateView, MensajeDetailView, lista_mensajes, detalle_mensaje


urlpatterns = [
    path('mensajes/', views.MensajeCreateView.as_view(), name='MensajeCrear'), 
    path('mensajes/<int:pk>', views.MensajeDetailView.as_view(), name='MensajeDetalles'),

    path('lista/', views.lista_mensajes, name='lista-mensajes'),
    path('detalle/<int:pk>/', views.detalle_mensaje, name='detalle-mensaje'),
]