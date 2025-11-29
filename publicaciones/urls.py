from django.urls import path
from publicaciones import views
from .views import PublicacionCreateView, PublicacionDetailView, ComentarioCreateView, ComentarioDetailView, LikeCreateView, LikeDetailView, lista_publicaciones, lista_comentarios, lista_likes, detalle_comentario, detalle_like

urlpatterns = [
    path('publicacion/', views.PublicacionCreateView.as_view(), name='PublicacionCrear'), 
    path('publicacion/<int:pk>', views.PublicacionDetailView.as_view(), name='PublicacionDetalles'),
    path('comentario/', views.ComentarioCreateView.as_view(), name='ComentarioCrear'), 
    path('comentario/<int:pk>', views.ComentarioDetailView.as_view(), name='ComentarioDetalles'),
    path('like/', views.LikeCreateView.as_view(), name='LikeCrear'), 
    path('like/<int:pk>', views.LikeDetailView.as_view(), name='LikeDetalles'),

    path('lista/', lista_publicaciones, name='lista-publicaciones'),
    
    # Comentarios
    path('comentarios/', lista_comentarios, name='lista-comentarios'),
    path('comentario/<int:pk>/detalle/', detalle_comentario, name='detalle-comentario'),

    # Likes
    path('likes/', lista_likes, name='lista-likes'),
    path('like/<int:pk>/detalle/', detalle_like, name='detalle-like'),

]