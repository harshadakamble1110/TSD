"""Generate PDF certificate."""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER
import io


def generate_certificate_pdf(student_name, course_name, duration_hours, score_percent, grade):
    """Generate certificate PDF and return bytes."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Background
    c.setFillColor(colors.HexColor("#F8F9FA"))
    c.rect(0, 0, width, height, fill=1)
    
    # Border
    c.setStrokeColor(colors.HexColor("#6366F1"))
    c.setLineWidth(3)
    margin = 0.5 * inch
    c.rect(margin, margin, width - 2*margin, height - 2*margin, fill=0)
    
    # Title
    c.setFillColor(colors.HexColor("#6366F1"))
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(width/2, height - 2*inch, "Certificate of Completion")
    
    # Subtitle
    c.setFillColor(colors.HexColor("#64748B"))
    c.setFont("Helvetica", 16)
    c.drawCentredString(width/2, height - 2.7*inch, "This is to certify that")
    
    # Name
    c.setFillColor(colors.HexColor("#0F172A"))
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height - 3.5*inch, student_name)
    
    # Course text
    c.setFillColor(colors.HexColor("#64748B"))
    c.setFont("Helvetica", 16)
    c.drawCentredString(width/2, height - 4.2*inch, "has successfully completed the course")
    
    # Course name
    c.setFillColor(colors.HexColor("#6366F1"))
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 4.9*inch, course_name)
    
    # Duration
    c.setFillColor(colors.HexColor("#64748B"))
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height - 5.4*inch, f"Course Duration: {duration_hours} hours")
    
    # Score and Grade
    c.setFillColor(colors.HexColor("#22D3EE"))
    c.setFont("Helvetica-Bold", 18)
    score_text = f"Score: {score_percent}% — Grade: {grade}"
    c.drawCentredString(width/2, height - 6.0*inch, score_text)
    
    # Footer
    c.setFillColor(colors.HexColor("#64748B"))
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, 1*inch, "TECH Skills Development")
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
