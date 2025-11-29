from django.urls import path
from historias import views
from .views import HistoriaCreateView, HistoriaDetailView, VistaHistoriaCreateView, VistaHistoriaDetailView, lista_historias, detalle_historia

urlpatterns = [
    path('historia/', views.HistoriaCreateView.as_view(), name='HistoriaCrear'), 
    path('historia/<int:pk>', views.HistoriaDetailView.as_view(), name='HistoriaDetalles'),
    path('vistahistoria/', views.VistaHistoriaCreateView.as_view(), name='VistaHistoriaCrear'), 
    path('vistahistoria/<int:pk>', views.VistaHistoriaDetailView.as_view(), name='VistaHistoriaDetalles'),

    path('lista/', views.lista_historias, name='lista-historias'),
    path('detalle/<int:pk>/', views.detalle_historia, name='detalle-historia'),
]