# chatbot/views_pdf.py
from django.shortcuts import render
from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse
from django.core.mail import EmailMessage, BadHeaderError
from django.conf import settings

from .pdf_admin_report import AdminPDFReport

User = get_user_model()

def descargar_certificado(request, curso_id):
    """
    Vista pública: recibe username + password (de un superuser) y email destino.
    Si las credenciales son válidas y pertenecen a un superuser:
      - genera PDF (datos reales de la BD),
      - lo encripta con la contraseña ingresada,
      - lo envía por email al destinatario indicado.
    """
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email_to = request.POST.get('email_to', '').strip()
        send_copy = request.POST.get('send_copy', '') == '1'  # opcional: copia al remitente

        if not username or not password or not email_to:
            return render(request, 'pdfs/solicitar_password.html', {
                'error': 'Debes ingresar usuario, contraseña y correo destino.',
                'curso_id': curso_id
            })

        # Autenticar las credenciales proporcionadas
        user_auth = authenticate(request, username=username, password=password)
        if user_auth is None or not getattr(user_auth, 'is_superuser', False):
            return render(request, 'pdfs/solicitar_password.html', {
                'error': 'Credenciales inválidas o no pertenece a un superusuario.',
                'curso_id': curso_id
            })

        # Generar PDF sin encriptar
        generator = AdminPDFReport(titulo="REPORTE DE ADMINISTRADOR - Sistema")
        pdf_buf = generator.generar_pdf_sin_encriptar()

        # Encriptar con la contraseña ingresada
        pdf_encrypted = generator.encriptar_con_password(pdf_buf, password)

        # Preparar correo
        subject = f"Reporte Administrador - generado por {username} - {curso_id}"
        body = (
            f"Hola,\n\nAdjunto encontrarás el reporte administrador generado por {username}.\n"
            "El archivo PDF está encriptado y requiere la contraseña del superuser para abrirlo.\n\n"
            "Saludos."
        )
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', getattr(settings, 'EMAIL_HOST_USER', 'no-reply@example.com'))
        to_list = [email_to]
        if send_copy:
            to_list.append(from_email)

        # Adjuntar PDF: convertir BytesIO a bytes
        pdf_encrypted.seek(0)
        pdf_bytes = pdf_encrypted.read()

        email = EmailMessage(subject=subject, body=body, from_email=from_email, to=to_list)
        email.content_subtype = 'plain'
        email.attach(f'reporte_admin_{username}_{curso_id}.pdf', pdf_bytes, 'application/pdf')

        try:
            email.send(fail_silently=False)
        except BadHeaderError:
            return render(request, 'pdfs/solicitar_password.html', {'error': 'Error en encabezados del correo.', 'curso_id': curso_id})
        except Exception as e:
            return render(request, 'pdfs/solicitar_password.html', {'error': f'Error enviando correo: {e}', 'curso_id': curso_id})

        # Si quieres, también devolver el PDF como descarga inmediata además de enviarlo por email:
        # response = HttpResponse(pdf_encrypted, content_type='application/pdf')
        # response['Content-Disposition'] = f'attachment; filename="reporte_admin_{username}_{curso_id}.pdf"'
        # return response

        # Mostrar mensaje de éxito en la misma plantilla
        return render(request, 'pdfs/solicitar_password.html', {
            'success': f'Correo enviado correctamente a {email_to}.',
            'curso_id': curso_id
        })

    # GET -> render form
    return render(request, 'pdfs/solicitar_password.html', {'curso_id': curso_id})
