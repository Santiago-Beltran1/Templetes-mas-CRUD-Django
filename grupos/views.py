from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Grupo, MiembroGrupo
from .serializer import GrupoSerializer, MiembroGrupoSerializer

# Create your views here.

class GrupoCreateView(generics.ListCreateAPIView):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer

class GrupoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer

class MiembroGrupoCreateView(generics.ListCreateAPIView):
    queryset = MiembroGrupo.objects.all()
    serializer_class = MiembroGrupoSerializer

class MiembroGrupoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MiembroGrupo.objects.all()
    serializer_class = MiembroGrupoSerializer

def lista_grupos(request):
    grupos = Grupo.objects.order_by('-fecha_creacion')
    return render(request, 'grupos/grupos_list.html', {'grupos': grupos})

def detalle_grupo(request, pk):
    grupo = get_object_or_404(Grupo, pk=pk)
    miembros = grupo.miembrogrupo_set.select_related('usuario').all()
    return render(request, 'grupos/grupos_detail.html', {'grupo': grupo, 'miembros': miembros})

def lista_miembros(request):
    miembros = MiembroGrupo.objects.select_related('grupo', 'usuario').order_by('-fecha_union')
    return render(request, 'grupos/miembros_list.html', {'miembros': miembros})

def detalle_miembro(request, pk):
    miembro = get_object_or_404(MiembroGrupo.objects.select_related('grupo', 'usuario'), pk=pk)
    return render(request, 'grupos/miembros_detail.html', {'miembro': miembro})