"""Generate Certificate PDF with custom symbol - Final Version"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER
import io
from datetime import datetime
import hashlib


def get_grade_from_percentage(percentage):
    """Calculate grade based on percentage"""
    if percentage >= 90:
        return "A"
    elif percentage >= 80:
        return "B"
    elif percentage >= 70:
        return "C"
    elif percentage >= 60:
        return "D"
    else:
        return "F"


def draw_custom_symbol(c, x, y, size):
    """Draw custom symbol (book/graduation cap design)"""
    cap_width = size * 0.8
    cap_height = size * 0.3
    book_width = size * 0.6
    book_height = size * 0.15
    
    # Book base
    c.setFillColor(colors.HexColor("#8B4513"))  # Brown color for book
    c.rect(x - book_width/2, y - book_height/2, book_width, book_height, fill=1)
    
    # Book pages effect
    c.setFillColor(colors.HexColor("#F5DEB3"))  # Light pages
    c.rect(x - book_width/2 + 2, y - book_height/2 + 2, book_width - 4, book_height - 4, fill=1)
    
    # Graduation cap
    c.setFillColor(colors.HexColor("#1F2937"))  # Dark color for cap
    
    # Draw cap base (mortarboard) using simple rectangle
    c.rect(x - cap_width/2, y + cap_height/2, cap_width, cap_height/2, fill=1)
    
    # Cap top (square part)
    top_size = cap_width * 0.7
    c.setFillColor(colors.HexColor("#2C3E50"))  # Slightly lighter for top
    c.rect(x - top_size/2, y + cap_height/2 + 5, top_size, top_size/3, fill=1)
    
    # Tassel
    c.setStrokeColor(colors.HexColor("#FFD700"))  # Gold tassel
    c.setLineWidth(2)
    c.line(x + top_size/2, y + cap_height/2 + 5, x + top_size/2 + 15, y + cap_height/2 + 15)
    
    # Tassel end
    c.setFillColor(colors.HexColor("#FFD700"))
    c.circle(x + top_size/2 + 15, y + cap_height/2 + 15, 3, fill=1)


def generate_certificate_pdf(student_name, course_name, duration_hours, score_percent, grade=None):
    """Generate certificate PDF with custom symbol."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Calculate grade if not provided
    if grade is None:
        grade = get_grade_from_percentage(score_percent)
    
    # Generate unique certificate ID
    cert_data = f"{student_name}_{course_name}_{datetime.now().strftime('%Y%m%d')}"
    cert_id = f"TSD-{hashlib.md5(cert_data.encode()).hexdigest()[:8].upper()}"
    
    # Clean white background
    c.setFillColor(colors.white)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    # Main border with proper margins
    border_margin = 0.8 * inch
    c.setStrokeColor(colors.HexColor("#4F46E5"))
    c.setLineWidth(4)
    c.rect(border_margin, border_margin, width - 2*border_margin, height - 2*border_margin, fill=0)
    
    # Inner decorative border
    inner_margin = 0.9 * inch
    c.setStrokeColor(colors.HexColor("#7C3AED"))
    c.setLineWidth(2)
    c.rect(inner_margin, inner_margin, width - 2*inner_margin, height - 2*inner_margin, fill=0)
    
    # Content area (inside borders)
    content_left = inner_margin + 0.5 * inch
    content_right = width - inner_margin - 0.5 * inch
    content_width = content_right - content_left
    content_center = width / 2
    
    # 1️⃣ Custom Symbol (Top Center - Inside borders)
    symbol_y = height - 1.5 * inch
    symbol_size = 40  # Size of custom symbol
    
    # Draw custom symbol
    draw_custom_symbol(c, content_center, symbol_y, symbol_size)
    
    # Organization Name
    org_y = symbol_y - symbol_size/2 - 0.3 * inch
    c.setFillColor(colors.HexColor("#1F2937"))
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(content_center, org_y, "TECH Skills Development")
    
    # Tagline
    tagline_y = org_y - 0.25 * inch
    c.setFillColor(colors.HexColor("#6B7280"))
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(content_center, tagline_y, "Empowering Future Tech Leaders")
    
    # 2️⃣ Certificate Title (Properly sized to fit inside borders)
    title_y = height - 2.8 * inch
    
    # Main title with proper size to fit borders
    c.setFillColor(colors.HexColor("#4F46E5"))
    c.setFont("Helvetica-Bold", 26)  # Reduced to fit borders
    c.drawCentredString(content_center, title_y, "CERTIFICATE OF COMPLETION")
    
    # Decorative line under title
    line_y = title_y - 0.3 * inch
    c.setStrokeColor(colors.HexColor("#7C3AED"))
    c.setLineWidth(2)
    c.line(content_center - 100, line_y, content_center + 100, line_y)
    
    # 3️⃣ Main Certificate Text (Inside borders)
    cert_text_y = height - 3.8 * inch
    
    # "This is to certify that" - elegant introduction
    c.setFillColor(colors.HexColor("#374151"))
    c.setFont("Helvetica", 14)
    c.drawCentredString(content_center, cert_text_y, "This is to certify that")
    
    # Student name - prominent display
    name_y = cert_text_y - 0.6 * inch
    c.setFillColor(colors.HexColor("#1F2937"))
    c.setFont("Helvetica-Bold", 24)  # Reduced to fit borders
    c.drawCentredString(content_center, name_y, student_name)
    
    # Main certificate text continuation
    main_text_y = name_y - 0.6 * inch
    c.setFillColor(colors.HexColor("#374151"))
    c.setFont("Helvetica", 14)
    
    # Build certificate text as specified
    cert_text = f"has successfully completed course \"{course_name}\" conducted by TECH Skills Development"
    
    # Split long text to fit inside borders
    if len(cert_text) > 60:
        # Split at logical point
        parts = cert_text.split(" conducted by")
        part1 = parts[0]
        part2 = "conducted by" + parts[1]
        
        c.drawCentredString(content_center, main_text_y, part1)
        c.drawCentredString(content_center, main_text_y - 0.5 * inch, part2)
        score_y = main_text_y - 1.0 * inch
    else:
        c.drawCentredString(content_center, main_text_y, cert_text)
        score_y = main_text_y - 0.5 * inch
    
    # Score and grade information
    score_text = f"with percentage {score_percent}% and its Grade {grade}"
    c.setFillColor(colors.HexColor("#059669"))
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(content_center, score_y, score_text)
    
    # Course name highlight box (properly sized to fit borders)
    course_box_y = score_y - 0.8 * inch
    course_box_width = min(content_width * 0.7, 4.5 * inch)  # Ensure it fits borders
    course_box_height = 0.6 * inch
    course_box_x = content_center - course_box_width/2
    
    # Subtle background for course name
    c.setFillColor(colors.Color(79, 70, 229, 0.08))
    c.roundRect(course_box_x, course_box_y - course_box_height/2, course_box_width, course_box_height, 8, fill=1)
    
    # Course name border
    c.setStrokeColor(colors.HexColor("#4F46E5"))
    c.setLineWidth(1)
    c.roundRect(course_box_x, course_box_y - course_box_height/2, course_box_width, course_box_height, 8, fill=0)
    
    # Course name (with proper font size to fit)
    c.setFillColor(colors.HexColor("#4F46E5"))
    c.setFont("Helvetica-Bold", 16)  # Reduced to fit borders
    
    # Truncate course name if too long
    display_course_name = course_name
    if len(course_name) > 25:
        display_course_name = course_name[:22] + "..."
    
    c.drawCentredString(content_center, course_box_y, display_course_name)
    
    # 4️⃣ Additional Details Section (Inside borders, perfectly aligned)
    details_y = course_box_y - 1.0 * inch
    
    # Details box (properly sized to fit borders)
    details_box_width = min(content_width * 0.6, 4 * inch)  # Ensure it fits borders
    details_box_height = 1.2 * inch
    details_box_x = content_center - details_box_width/2
    
    # Details background
    c.setFillColor(colors.Color(248, 250, 252, 1))
    c.roundRect(details_box_x, details_y - details_box_height/2, details_box_width, details_box_height, 8, fill=1)
    
    # Details border
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(1)
    c.roundRect(details_box_x, details_y - details_box_height/2, details_box_width, details_box_height, 8, fill=0)
    
    # Certificate details with proper alignment
    c.setFillColor(colors.HexColor("#374151"))
    c.setFont("Helvetica", 10)  # Reduced to fit borders
    
    # Certificate ID
    cert_id_y = details_y + 0.4 * inch
    c.drawCentredString(content_center, cert_id_y, f"Certificate ID: {cert_id}")
    
    # Duration
    duration_y = details_y + 0.2 * inch
    c.drawCentredString(content_center, duration_y, f"Duration: {duration_hours} Hours")
    
    # Mode
    mode_y = details_y
    c.drawCentredString(content_center, mode_y, "Mode: Online")
    
    # Issue Date
    issue_date = datetime.now().strftime("%B %d, %Y")
    issue_y = details_y - 0.2 * inch
    c.drawCentredString(content_center, issue_y, f"Issue Date: {issue_date}")
    
    # Verification section (only issue date and verify link, no signature)
    verify_y = details_y - 1.2 * inch
    
    # Issue Date (second time - in verification section)
    c.setFillColor(colors.HexColor("#6B7280"))
    c.setFont("Helvetica", 10)
    c.drawCentredString(content_center, verify_y, f"Date: {issue_date}")
    
    # Verification URL
    verify_url_y = verify_y - 0.4 * inch
    c.setFillColor(colors.HexColor("#4F46E5"))
    c.setFont("Helvetica", 8)  # Smaller to fit borders
    c.drawCentredString(content_center, verify_url_y, "Verify at: www.techskillsdevelopment.com/verify")
    
    # NO FOOTER SECTION - Removed TSD logo and tagline to prevent overlap
    
    # NO GRADE INDICATOR - Removed F symbol and grey circle completely
    
    # Security watermark (very subtle)
    c.setFillColor(colors.Color(0, 0, 0, 0.02))
    c.setFont("Helvetica-Bold", 36)  # Smaller watermark
    c.drawCentredString(content_center, height/2, "TSD VERIFIED")
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
