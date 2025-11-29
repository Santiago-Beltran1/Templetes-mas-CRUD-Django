from rest_framework import serializers
from .models import Grupo, MiembroGrupo

class GrupoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Grupo
        fields = ["id", "VISIBILIDAD_GRUPO", "nombre", "descripcion", "creador", "visibilidad", "fecha_creacion", "avatar", "reglas", "activo"]

class MiembroGrupoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = MiembroGrupo
        fields = ["id", "ROL_MIEMBRO", "grupo", "usuario", "rol", "fecha_union", "notificaciones_activas"]
