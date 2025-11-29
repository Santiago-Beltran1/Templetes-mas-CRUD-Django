from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Mensaje
from .serializer import MensajeSerializer

# Create your views here.

class MensajeCreateView(generics.ListCreateAPIView):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer

class MensajeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer

def lista_mensajes(request):
    mensajes = Mensaje.objects.select_related('remitente', 'destinatario').order_by('-fecha_envio')
    return render(request, 'mensajes/mensajes_list.html', {'mensajes': mensajes})

def detalle_mensaje(request, pk):
    mensaje = get_object_or_404(Mensaje.objects.select_related('remitente', 'destinatario'), pk=pk)
    return render(request, 'mensajes/mensajes_detail.html', {'mensaje': mensaje})