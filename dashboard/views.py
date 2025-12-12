# dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.db.models.functions import TruncDate
import json
from django.utils.safestring import mark_safe

from django.contrib.auth import get_user_model
User = get_user_model()

from usuario.models import Usuario
from publicaciones.models import Publicacion, Comentario, Like
from relacion.models import Seguidor
from mensajes.models import Mensaje
from grupos.models import Grupo
from historias.models import Historia

# decorador: solo superuser puede acceder
def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_active and u.is_superuser, login_url='/accounts/login/')(view_func)

@superuser_required
def home_dashboard(request):
    # Totales rápidos
    total_users = User.objects.count()
    total_perfiles = Usuario.objects.count()
    total_publicaciones = Publicacion.objects.count()
    total_comentarios = Comentario.objects.count()
    total_likes = Like.objects.count()
    total_seguidores = Seguidor.objects.count()
    total_mensajes = Mensaje.objects.count()
    total_grupos = Grupo.objects.count()
    total_historias = Historia.objects.count()

    # Usuarios por ciudad (top 10)
    usuarios_por_ciudad = Usuario.objects.values('ciudad').annotate(total=Count('id')).order_by('-total')[:10]
    ciudades = [u['ciudad'] or '—' for u in usuarios_por_ciudad]
    ciudades_counts = [u['total'] for u in usuarios_por_ciudad]

    # Publicaciones por día (últimos 30 días)
    publicaciones_por_dia_qs = Publicacion.objects.annotate(date=TruncDate('fecha_creacion')).values('date').annotate(total=Count('id')).order_by('date')
    # convertir a listas (formato para Chart.js)
    fechas = [p['date'].strftime('%Y-%m-%d') for p in publicaciones_por_dia_qs]
    publicaciones_counts = [p['total'] for p in publicaciones_por_dia_qs]

    # Top autores por número de publicaciones (top 10)
    top_autores_qs = Publicacion.objects.values('usuario__user__username').annotate(total=Count('id')).order_by('-total')[:10]
    autores = [a['usuario__user__username'] for a in top_autores_qs]
    autores_counts = [a['total'] for a in top_autores_qs]

    context = {
        'total_users': total_users,
        'total_perfiles': total_perfiles,
        'total_publicaciones': total_publicaciones,
        'total_comentarios': total_comentarios,
        'total_likes': total_likes,
        'total_seguidores': total_seguidores,
        'total_mensajes': total_mensajes,
        'total_grupos': total_grupos,
        'total_historias': total_historias,

        # datos para gráficos (serializados a JSON seguro)
        'ciudades_labels': mark_safe(json.dumps(ciudades)),
        'ciudades_data': mark_safe(json.dumps(ciudades_counts)),
        'fechas_labels': mark_safe(json.dumps(fechas)),
        'fechas_data': mark_safe(json.dumps(publicaciones_counts)),
        'autores_labels': mark_safe(json.dumps(autores)),
        'autores_data': mark_safe(json.dumps(autores_counts)),
    }
    return render(request, 'dashboard/home.html', context)

@superuser_required
def usuarios_table(request):
    # lista de usuarios con perfil y stats
    users = User.objects.all().order_by('-id')[:200]
    usuarios = []
    for u in users:
        try:
            perfil = Usuario.objects.get(user_id=u.id)
        except Usuario.DoesNotExist:
            perfil = None
        usuarios.append({
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'is_superuser': u.is_superuser,
            'fecha_nacimiento': getattr(perfil, 'fecha_nacimiento', '') if perfil else '',
            'ciudad': getattr(perfil, 'ciudad', '') if perfil else '',
        })
    return render(request, 'dashboard/usuarios_table.html', {'usuarios': usuarios})

@superuser_required
def publicaciones_table(request):
    posts = Publicacion.objects.select_related('usuario__user').order_by('-fecha_creacion')[:200]
    data = []
    for p in posts:
        data.append({
            'id': p.id,
            'usuario': getattr(p.usuario.user, 'username', str(getattr(p.usuario, 'id', '—'))),
            'tipo': p.tipo,
            'visibilidad': p.visibilidad,
            'fecha': p.fecha_creacion,
            'contenido': (p.contenido[:250] + '...') if p.contenido and len(p.contenido) > 250 else (p.contenido or ''),
        })
    return render(request, 'dashboard/publicaciones_table.html', {'posts': data})
