# pdf_generator.py (usar dentro de tu app)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from PyPDF2 import PdfWriter, PdfReader
from io import BytesIO
from datetime import datetime
from django.contrib.auth.models import User

# importa modelos tuyos
from usuario.models import Usuario
from publicaciones.models import Publicacion
from relacion.models import Seguidor
from mensajes.models import Mensaje

class PDFGenerador:
    def __init__(self, titulo="Documento"):
        self.titulo = titulo
        self.styles = getSampleStyleSheet()
        self.pagesize = A4

    def generar_pdf_y_encriptar(self, user_obj, password_plain, contenido_extra=None):
        # --- Construcción del PDF con datos desde la BD ---
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=self.pagesize,
                                rightMargin=0.5*inch, leftMargin=0.5*inch,
                                topMargin=0.75*inch, bottomMargin=0.75*inch)
        story = []

        # título
        titulo_text = contenido_extra.get('titulo') if contenido_extra and 'titulo' in contenido_extra else f"Informe de usuario - {user_obj.username}"
        story.append(Paragraph(titulo_text, ParagraphStyle('Title', parent=self.styles['Heading1'], fontSize=18, alignment=1, textColor=colors.HexColor('#208091'))))
        story.append(Spacer(1, 0.15*inch))

        # info básica desde auth.User
        story.append(Paragraph("<b>Datos de cuenta</b>", self.styles['Heading2']))
        datos = [
            ['Usuario', user_obj.username],
            ['Nombre', f"{user_obj.first_name} {user_obj.last_name}".strip() or '—'],
            ['Email', user_obj.email or '—'],
            ['Generado', datetime.now().strftime("%d/%m/%Y %H:%M")]
        ]

        # datos extendidos desde tu modelo usuario.Usuario (si existe)
        try:
            perfil = Usuario.objects.get(user_id=user_obj.id)
            datos += [
                ['Fecha Nacimiento', perfil.fecha_nacimiento or '—'],
                ['Teléfono', perfil.telefono or '—'],
                ['País', perfil.pais or '—'],
                ['Ciudad', perfil.ciudad or '—'],
                ['Biografía', (perfil.biografia[:200] + '...') if perfil.biografia else '—'],
            ]
        except Usuario.DoesNotExist:
            perfil = None

        tabla = Table(datos, colWidths=[2.2*inch, 3.2*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#E8F4F8')),
            ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ]))
        story.append(tabla)
        story.append(Spacer(1, 0.2*inch))

        # Estadísticas: publicaciones, seguidores, mensajes
        pub_count = Publicacion.objects.filter(usuario__user_id=user_obj.id).count()  # si tu modelo hace FK a Usuario diferente ajustar
        seguidores_count = Seguidor.objects.filter(seguido__user_id=user_obj.id).count()
        mensajes_recibidos = Mensaje.objects.filter(destinatario__user_id=user_obj.id).count()

        story.append(Paragraph("<b>Estadísticas</b>", self.styles['Heading2']))
        stats = [
            ['Publicaciones', str(pub_count)],
            ['Seguidores', str(seguidores_count)],
            ['Mensajes recibidos', str(mensajes_recibidos)],
        ]
        story.append(Table(stats, colWidths=[3*inch, 2.5*inch]))
        story.append(Spacer(1, 0.2*inch))

        # Lista las últimas 5 publicaciones (contenido breve)
        ultimas = Publicacion.objects.filter(usuario__user_id=user_obj.id).order_by('-fecha_creacion')[:5]
        if ultimas:
            story.append(Paragraph("<b>Últimas publicaciones</b>", self.styles['Heading2']))
            for p in ultimas:
                texto = (p.contenido[:200] + '...') if len(p.contenido) > 200 else p.contenido
                story.append(Paragraph(f"- {texto}", self.styles['Normal']))
                story.append(Spacer(1, 0.05*inch))

        # contenido adicional opcional
        if contenido_extra and 'contenido' in contenido_extra:
            story.append(Spacer(1, 0.15*inch))
            story.append(Paragraph(contenido_extra['contenido'], self.styles['Normal']))

        doc.build(story)

        # --- Encriptar con contraseña provista ---
        buffer.seek(0)
        pdf_reader = PdfReader(buffer)
        pdf_writer = PdfWriter()
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        pdf_writer.encrypt(user_password=str(password_plain), owner_password=str(password_plain))

        out = BytesIO()
        pdf_writer.write(out)
        out.seek(0)
        return out
