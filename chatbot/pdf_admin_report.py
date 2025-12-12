# chatbot/pdf_admin_report.py
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter

# modelos (ajusta imports si tus apps se llaman distinto)
from django.contrib.auth.models import User
from usuario.models import Usuario
from publicaciones.models import Publicacion, Comentario, Like
from relacion.models import Seguidor
from mensajes.models import Mensaje
from grupos.models import Grupo, MiembroGrupo
from historias.models import Historia, VistaHistoria

class AdminPDFReport:
    def __init__(self, titulo="Reporte Administrador"):
        self.titulo = titulo
        self.styles = getSampleStyleSheet()
        self.pagesize = A4

    def _make_table(self, data, col_widths=None, header_bg=colors.HexColor('#208091')):
        t = Table(data, colWidths=col_widths)
        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), header_bg),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8F8F8')])
        ])
        t.setStyle(style)
        return t

    def generar_pdf_sin_encriptar(self):
        """
        Genera el PDF en memoria (BytesIO) con todo el contenido, sin encriptar.
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=self.pagesize,
                                rightMargin=0.5*inch, leftMargin=0.5*inch,
                                topMargin=0.6*inch, bottomMargin=0.6*inch)
        story = []

        # Portada
        title_style = ParagraphStyle('Title', parent=self.styles['Title'], fontSize=20, alignment=1, textColor=colors.HexColor('#208091'))
        story.append(Paragraph(self.titulo, title_style))
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(f"<i>Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</i>",
                               ParagraphStyle('Date', parent=self.styles['Normal'], alignment=1, fontSize=9)))
        story.append(Spacer(1, 0.25*inch))

        # Resumen estadístico
        story.append(Paragraph("<b>Resumen Estadístico</b>", self.styles['Heading2']))
        total_users = User.objects.count()
        total_perfiles = Usuario.objects.count()
        total_publicaciones = Publicacion.objects.count()
        total_comentarios = Comentario.objects.count()
        total_likes = Like.objects.count()
        total_seguidores = Seguidor.objects.count()
        total_mensajes = Mensaje.objects.count()
        total_grupos = Grupo.objects.count()
        total_miembros = MiembroGrupo.objects.count()
        total_historias = Historia.objects.count()
        total_vistas_historias = VistaHistoria.objects.count()

        stats_data = [
            ['Elemento', 'Total'],
            ['Usuarios (auth_user)', str(total_users)],
            ['Perfiles (usuario)', str(total_perfiles)],
            ['Publicaciones', str(total_publicaciones)],
            ['Comentarios', str(total_comentarios)],
            ['Reacciones (Likes)', str(total_likes)],
            ['Relaciones (Seguidores)', str(total_seguidores)],
            ['Mensajes', str(total_mensajes)],
            ['Grupos', str(total_grupos)],
            ['Miembros en grupos', str(total_miembros)],
            ['Historias', str(total_historias)],
            ['Vistas de Historias', str(total_vistas_historias)],
        ]
        story.append(self._make_table(stats_data, col_widths=[3.5*inch, 2*inch]))
        story.append(PageBreak())

        # Usuarios (resumen)
        story.append(Paragraph("<b>Lista de Usuarios</b>", self.styles['Heading2']))
        users = User.objects.order_by('id').all()
        if users:
            u_data = [['ID', 'Username', 'Nombre', 'Email', 'is_superuser', 'is_staff', 'is_active']]
            for u in users:
                u_data.append([str(u.id), u.username, f"{u.first_name} {u.last_name}".strip(), u.email or '—', str(u.is_superuser), str(u.is_staff), str(u.is_active)])
            story.append(self._make_table(u_data, col_widths=[0.6*inch, 1.5*inch, 2*inch, 2.5*inch, 0.8*inch, 0.8*inch, 0.8*inch]))
        else:
            story.append(Paragraph("No hay usuarios registrados.", self.styles['Normal']))
        story.append(PageBreak())

        # Perfiles
        story.append(Paragraph("<b>Perfiles</b>", self.styles['Heading2']))
        perfiles = Usuario.objects.select_related('user').order_by('id').all()
        if perfiles:
            p_data = [['ID', 'Usuario(auth)', 'Fecha Nac', 'Teléfono', 'País', 'Ciudad', 'Privado']]
            for p in perfiles:
                p_data.append([str(p.id), p.user.username if p.user else '—', str(p.fecha_nacimiento) if p.fecha_nacimiento else '—', p.telefono or '—', p.pais or '—', p.ciudad or '—', str(p.privado)])
            story.append(self._make_table(p_data, col_widths=[0.5*inch, 1.5*inch, 1.1*inch, 1.2*inch, 1.1*inch, 1.1*inch, 0.8*inch]))
        else:
            story.append(Paragraph("No hay perfiles.", self.styles['Normal']))
        story.append(PageBreak())

        # Publicaciones (últimas 100)
        story.append(Paragraph("<b>Publicaciones (últimas 100)</b>", self.styles['Heading2']))
        publicaciones = Publicacion.objects.select_related('usuario').order_by('-fecha_creacion')[:100]
        if publicaciones:
            pub_data = [['ID','Usuario','Tipo','Visibilidad','Fecha','Contenido corto','Adjunto']]
            for p in publicaciones:
                snippet = (p.contenido[:120] + '...') if p.contenido and len(p.contenido) > 120 else (p.contenido or '—')
                pub_data.append([str(p.id), getattr(p.usuario.user, 'username', str(p.usuario.id) if p.usuario else '—'), p.tipo, p.visibilidad, p.fecha_creacion.strftime('%Y-%m-%d %H:%M'), snippet, p.archivo_adjunto or '—'])
            story.append(self._make_table(pub_data, col_widths=[0.4*inch, 1.2*inch, 0.8*inch, 0.9*inch, 1.1*inch, 2.4*inch, 1.1*inch]))
        else:
            story.append(Paragraph("No hay publicaciones.", self.styles['Normal']))
        story.append(PageBreak())

        # Puedes añadir más secciones aquí (comentarios, likes, mensajes...) similar a las anteriores
        # Para mantenerlo razonable dejamos algunas secciones; si quieres que agregue todas, lo hago.

        doc.build(story)
        buffer.seek(0)
        return buffer

    def encriptar_con_password(self, buffer_pdf_bytesio, password_plain):
        """
        Encripta el PDF en buffer_pdf_bytesio usando password_plain.
        Devuelve BytesIO con PDF encriptado.
        """
        buffer_pdf_bytesio.seek(0)
        reader = PdfReader(buffer_pdf_bytesio)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(user_password=str(password_plain), owner_password=str(password_plain))

        out = BytesIO()
        writer.write(out)
        out.seek(0)
        return out
