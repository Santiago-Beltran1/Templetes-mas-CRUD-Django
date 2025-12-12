"""
URL configuration for examen_clase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# importamos home desde la app usuario
from usuario.views import home
from chatbot.views_pdf import descargar_certificado

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home (página principal)
    path('', home, name='home'),

    # Rutas de las apps
    path('usuario/', include('usuario.urls')),
    path('publicaciones/', include('publicaciones.urls')),
    path('relacion/', include('relacion.urls')),
    path('mensajes/', include('mensajes.urls')),
    path('grupos/', include('grupos.urls')),
    path('historias/', include('historias.urls')),

    # en examen_clase/urls.py
    path('chatbot/', include('chatbot.urls')),

    path('certificado/<int:curso_id>/', descargar_certificado, name='descargar_certificado'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
