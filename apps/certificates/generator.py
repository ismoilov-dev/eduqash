import os
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors


class CertificateGenerator:
    @staticmethod
    def generate_pdf_and_qr(certificate):
        verify_url = f"{getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')}/verify-certificate/{certificate.unique_id}"

        # Generate QR Code image
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(verify_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        qr_io = BytesIO()
        qr_img.save(qr_io, format='PNG')
        qr_filename = f"qr_{certificate.unique_id}.png"
        certificate.qr_code.save(qr_filename, ContentFile(qr_io.getvalue()), save=False)

        # Generate PDF document using ReportLab
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=landscape(letter))
        width, height = landscape(letter)

        # Border design
        p.setStrokeColor(colors.HexColor("#1A365D"))
        p.setLineWidth(5)
        p.rect(20, 20, width - 40, height - 40)

        p.setStrokeColor(colors.HexColor("#2B6CB0"))
        p.setLineWidth(1)
        p.rect(25, 25, width - 50, height - 50)

        # Header Title
        p.setFont("Helvetica-Bold", 32)
        p.setFillColor(colors.HexColor("#1A365D"))
        p.drawCentredString(width / 2, height - 90, "CERTIFICATE OF COMPLETION")

        p.setFont("Helvetica", 14)
        p.setFillColor(colors.HexColor("#4A5568"))
        p.drawCentredString(width / 2, height - 130, "This is proudly presented to")

        # User Name
        user_fullname = f"{certificate.user.first_name} {certificate.user.last_name}".strip() or certificate.user.username
        p.setFont("Helvetica-Bold", 26)
        p.setFillColor(colors.HexColor("#2B6CB0"))
        p.drawCentredString(width / 2, height - 180, user_fullname.upper())

        p.setFont("Helvetica", 14)
        p.setFillColor(colors.HexColor("#4A5568"))
        p.drawCentredString(width / 2, height - 220, "for successfully completing the course/exam")

        # Course/Exam Title
        cert_title = certificate.title or (certificate.course.title if certificate.course else (certificate.exam.title if certificate.exam else "EDUQASH PRO Program"))
        p.setFont("Helvetica-Bold", 20)
        p.setFillColor(colors.HexColor("#1A365D"))
        p.drawCentredString(width / 2, height - 260, cert_title)

        # Issue Date & ID
        p.setFont("Helvetica", 11)
        p.setFillColor(colors.HexColor("#718096"))
        p.drawString(60, 80, f"Issue Date: {certificate.issue_date}")
        p.drawString(60, 60, f"Certificate ID: {certificate.unique_id}")

        # Draw QR Code image onto PDF
        qr_io.seek(0)
        from reportlab.lib.utils import ImageReader
        img_reader = ImageReader(qr_io)
        p.drawImage(img_reader, width - 150, 50, width=90, height=90)

        p.showPage()
        p.save()

        buffer.seek(0)
        pdf_filename = f"cert_{certificate.unique_id}.pdf"
        certificate.pdf_file.save(pdf_filename, ContentFile(buffer.getvalue()), save=True)
