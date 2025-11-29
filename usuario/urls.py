from django.urls import path
from usuario import views
from .views import UsuarioCreateView, UsuarioDetailView, PerfilCreateView, PerfilDetailView, lista_usuarios, detalle_usuario, lista_perfiles, detalle_perfil

urlpatterns = [
    path('usuario/', views.UsuarioCreateView.as_view(), name='UsuarioCrear'), 
    path('usuario/<int:pk>', views.UsuarioDetailView.as_view(), name='UsuarioDetalles'),
    path('perfil/', views.PerfilCreateView.as_view(), name='PerfilCrear'), 
    path('perfil/<int:pk>', views.PerfilDetailView.as_view(), name='PerfilDetalles'),
    
    path('lista/', lista_usuarios, name='lista-usuarios'),
    path('<int:pk>/', detalle_usuario, name='detalle-usuario'),

    path('perfiles/', lista_perfiles, name='lista-perfiles'),
    path('perfil/<int:pk>/', detalle_perfil, name='detalle-perfil'),

]