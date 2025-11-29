from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Seguidor
from .serializer import SeguidorSerializer

# --- API ---
class SeguidorCreateView(generics.ListCreateAPIView):
    queryset = Seguidor.objects.all()
    serializer_class = SeguidorSerializer

class SeguidorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Seguidor.objects.all()
    serializer_class = SeguidorSerializer

# --- Vistas que renderizan templates ---
def lista_relaciones(request):
    seguimientos = Seguidor.objects.select_related('seguidor', 'seguido').order_by('-fecha_seguimiento')
    return render(request, 'relacion/seguidores_list.html', {'seguimientos': seguimientos})

def detalle_relacion(request, pk):
    seguimiento = get_object_or_404(Seguidor.objects.select_related('seguidor', 'seguido'), pk=pk)
    return render(request, 'relacion/seguidores_detail.html', {'seguimiento': seguimiento})
