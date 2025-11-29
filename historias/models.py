from django.db import models
from django.utils.translation import gettext_lazy as _
from usuario.models import Usuario

# Create your models here.

class Historia(models.Model):
    TIPO_HISTORIA = [
        ('texto', 'Texto'),
        ('imagen', 'Imagen'),
        ('video', 'Video'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_HISTORIA)
    contenido = models.TextField(blank=True)
    archivo = models.FileField(upload_to='historias/', blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        # Devuelve el nombre del usuario o el ID si no tiene nombre
        return f"Historia de {self.usuario.username if hasattr(self.usuario, 'username') else self.usuario.id}"


class VistaHistoria(models.Model):
    historia = models.ForeignKey(Historia, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_vista = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vista de {self.usuario.username if hasattr(self.usuario, 'username') else self.usuario.id}"
