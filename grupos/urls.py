from django.urls import path
from grupos import views
from .views import GrupoCreateView, GrupoDetailView, MiembroGrupoCreateView, MiembroGrupoDetailView, lista_grupos, detalle_grupo, lista_miembros, detalle_miembro

urlpatterns = [
    path('grupo/', views.GrupoCreateView.as_view(), name='GrupoCrear'), 
    path('grupo/<int:pk>', views.GrupoDetailView.as_view(), name='GrupoDetalles'),
    path('miembrogrupo/', views.MiembroGrupoCreateView.as_view(), name='MiembroGrupoCrear'), 
    path('miembrogrupo/<int:pk>', views.MiembroGrupoDetailView.as_view(), name='MiembroGrupoDetalles'),

    path('lista/', views.lista_grupos, name='lista-grupos'),
    path('detalle/<int:pk>/', views.detalle_grupo, name='detalle-grupo'),

    path('miembros/', views.lista_miembros, name='lista-miembros'),
    path('miembros/detalle/<int:pk>/', views.detalle_miembro, name='detalle-miembro'),
]