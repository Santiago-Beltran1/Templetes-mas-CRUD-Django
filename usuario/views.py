from django.shortcuts import render
from rest_framework import generics
from .models import Usuario, Perfil
from .serializer import UsuarioSerializer, PerfilSerializer

# Create your views here.

class UsuarioCreateView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class PerfilCreateView(generics.ListCreateAPIView):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer

class PerfilDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer


def home(request):
    return render(request, 'home.html')


def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuario/lista_usuarios.html', {'usuarios': usuarios})


def detalle_usuario(request, pk):
    usuario = Usuario.objects.get(pk=pk)
    return render(request, 'usuario/detalle_usuario.html', {'usuario': usuario})

def lista_perfiles(request):
    perfiles = Perfil.objects.select_related('usuario__user').all()
    return render(request, 'usuario/lista_perfiles.html', {'perfiles': perfiles})


def detalle_perfil(request, pk):
    perfil = Perfil.objects.select_related('usuario__user').get(pk=pk)
    return render(request, 'usuario/detalle_perfil.html', {'perfil': perfil})
