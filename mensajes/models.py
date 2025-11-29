from django.db import models
from django.utils.translation import gettext_lazy as _
from usuario.models import Usuario

# Create your models here.

class Mensaje(models.Model):
    remitente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensajes_enviados')
    destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    fecha_lectura = models.DateTimeField(null=True, blank=True)
    archivo_adjunto = models.FileField(upload_to='mensajes/', blank=True)

    def __str__(self):
        return self.remitente