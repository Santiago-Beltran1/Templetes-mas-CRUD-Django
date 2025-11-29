from rest_framework import serializers
from .models import Publicacion, Comentario, Like

class PublicacionSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Publicacion
        fields = ["id", "TIPO_PUBLICACION", "VISIBILIDAD", "usuario", "contenido", "tipo", "visibilidad", "fecha_creacion", "fecha_actualizacion", "ubicacion", "archivo_adjunto", "activo"]

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Comentario
        fields = ["id", "publicacion", "usuario", "contenido", "fecha_creacion", "comentario_padre", "activo"]

class LikeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Like
        fields = ["id", "TIPO_LIKE", "publicacion", "usuario", "tipo", "fecha_creacion"]
