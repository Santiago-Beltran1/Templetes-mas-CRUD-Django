from django.db import models
from django.utils.translation import gettext_lazy as _
from usuario.models import Usuario

# Create your models here.

class Seguidor(models.Model):
    seguidor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='siguiendo')
    seguido = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='seguidores')
    fecha_seguimiento = models.DateTimeField(auto_now_add=True)
    notificaciones_activas = models.BooleanField(default=True)

    def __str__(self):
        return self.seguidor