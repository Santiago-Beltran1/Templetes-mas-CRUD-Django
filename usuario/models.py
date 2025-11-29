from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15, blank=True)
    pais = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    biografia = models.TextField(blank=True)
    sitio_web = models.URLField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultima_conexion = models.DateTimeField(auto_now=True)
    privado = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/')
    portada = models.ImageField(upload_to='portadas/')
    genero = models.CharField(max_length=20, choices=[
        ('masculino', 'Maculino'),
        ('femenino', 'Femenino'),
        ('otro', 'Otro'),
    ], blank=True)
    interes = models.TextField(blank=True)
    educacion = models.TextField(blank=True)
    trabajo = models.TextField(blank=True)

    def __str__(self):
        return self.usuario