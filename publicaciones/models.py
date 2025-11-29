from django.db import models
from django.utils.translation import gettext_lazy as _
from usuario.models import Usuario


class Publicacion(models.Model):
    TIPO_PUBLICACION = [
        ('texto', 'Texto'),
        ('imagen', 'Imagen'),
        ('video', 'Video'),
        ('enlace', 'Enlace'),
    ]
    VISIBILIDAD = [
        ('publico', 'Público'),
        ('amigos', 'Solo Amigos'),
        ('privado', 'Privado'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_PUBLICACION, default='texto')
    visibilidad = models.CharField(max_length=20, choices=VISIBILIDAD, default='publico')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    ubicacion = models.CharField(max_length=100, blank=True)
    archivo_adjunto = models.FileField(upload_to='publicaciones/', blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        # Mostrar el nombre o ID del usuario y parte del contenido
        return f"Publicación de {self.usuario}: {self.contenido[:30]}"


class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    comentario_padre = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        # Mostrar quién hizo el comentario y parte del texto
        return f"Comentario de {self.usuario}: {self.contenido[:30]}"


class Like(models.Model):
    TIPO_LIKE = [
        ('like', 'Like'),
        ('love', 'Love'),
        ('haha', 'Haha'),
        ('wow', 'Wow'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
    ]

    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_LIKE, default='like')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Mostrar el usuario y el tipo de reacción
        return f"{self.tipo} de {self.usuario}"
