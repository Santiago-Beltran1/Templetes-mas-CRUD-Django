from rest_framework import serializers
from .models import Usuario, Perfil

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Usuario
        fields = ["id", "user", "fecha_nacimiento", "telefono", "pais", "ciudad", "biografia", "sitio_web", "fecha_registro", "ultima_conexion", "privado"]

class PerfilSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Perfil
        fields = ["id", "usuario", "avatar", "portada", "genero", "interes", "educacion", "trabajo"]