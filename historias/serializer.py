from rest_framework import serializers
from .models import Historia, VistaHistoria

class HistoriaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Historia
        fields = ["id", "TIPO_HISTORIA", "usuario", "tipo", "contenido", "archivo", "fecha_creacion", "fecha_expiracion", "activa"]

class VistaHistoriaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = VistaHistoria
        fields = ["id", "historia", "usuario", "fecha_vista"]
