from rest_framework import serializers
from .models import Seguidor

class SeguidorSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Seguidor
        fields = ["id", "seguidor", "seguido", "fecha_seguimiento", "notificaciones_activas"]
