from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Historia, VistaHistoria
from .serializer import HistoriaSerializer, VistaHistoriaSerializer

# Create your views here.

class HistoriaCreateView(generics.ListCreateAPIView):
    queryset = Historia.objects.all()
    serializer_class = HistoriaSerializer

class HistoriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Historia.objects.all()
    serializer_class = HistoriaSerializer

class VistaHistoriaCreateView(generics.ListCreateAPIView):
    queryset = VistaHistoria.objects.all()
    serializer_class = VistaHistoriaSerializer

class VistaHistoriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VistaHistoria.objects.all()
    serializer_class = VistaHistoriaSerializer

def lista_historias(request):
    historias = Historia.objects.select_related('usuario').order_by('-fecha_creacion')
    return render(request, 'historias/historias_list.html', {'historias': historias})

def detalle_historia(request, pk):
    historia = get_object_or_404(Historia.objects.select_related('usuario'), pk=pk)
    vistas = VistaHistoria.objects.filter(historia=historia).select_related('usuario')
    return render(request, 'historias/historias_detail.html', {'historia': historia, 'vistas': vistas})