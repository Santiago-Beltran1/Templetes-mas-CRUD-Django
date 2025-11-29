from django.db import models
from django.utils.translation import gettext_lazy as _
from usuario.models import Usuario

# Create your models here.

class Grupo(models.Model):
    VISIBILIDAD_GRUPO = [
        ('publico','Público'),
        ('privado','Privado'),
        ('secreto','Secreto'),
    ]
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    visibilidad = models.CharField(max_length=20, choices=VISIBILIDAD_GRUPO, default='publico')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='grupos/', blank=True)
    reglas = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class MiembroGrupo(models.Model):
    ROL_MIEMBRO = [
        ('administrador','Administrador'),
        ('moderador','Moderador'),
        ('miembro','Miembro'),
    ]
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROL_MIEMBRO, default='miembro')
    fecha_union = models.DateTimeField(auto_now_add=True)
    notificaciones_activas = models.BooleanField(default=True)

    def __str__(self):
        return self.grupo