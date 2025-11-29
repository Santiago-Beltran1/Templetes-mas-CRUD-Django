from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Publicacion, Comentario, Like
from .serializer import PublicacionSerializer, ComentarioSerializer, LikeSerializer

# Create your views here.

class PublicacionCreateView(generics.ListCreateAPIView):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionSerializer

class PublicacionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionSerializer

class ComentarioCreateView(generics.ListCreateAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

class ComentarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

class LikeCreateView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class LikeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


def lista_publicaciones(request):
    publicaciones = Publicacion.objects.select_related('usuario__user').all()  # Mejora: evita consultas extra
    return render(request, 'publicaciones/lista_publicaciones.html', {'publicaciones': publicaciones})

def lista_comentarios(request):
    comentarios = Comentario.objects.select_related('usuario__user', 'publicacion').all()
    return render(request, 'publicaciones/lista_comentarios.html', {'comentarios': comentarios})


def detalle_comentario(request, pk):
    comentario = get_object_or_404(Comentario.objects.select_related('usuario__user', 'publicacion'), pk=pk)
    return render(request, 'publicaciones/detalle_comentario.html', {'comentario': comentario})


def lista_likes(request):
    likes = Like.objects.select_related('usuario__user', 'publicacion').all()
    return render(request, 'publicaciones/lista_likes.html', {'likes': likes})


def detalle_like(request, pk):
    like = get_object_or_404(Like.objects.select_related('usuario__user', 'publicacion'), pk=pk)
    return render(request, 'publicaciones/detalle_like.html', {'like': like})
