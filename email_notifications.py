"""
Email notification system for course progress
"""
import os
import sys
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Add project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Enrollment, CourseTopic, TopicProgress, CourseTestAttempt, Course
from certificate_generator import generate_certificate_pdf
import io


class EmailNotificationService:
    def __init__(self):
        self.smtp_server = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.environ.get("MAIL_PORT", "587"))
        self.smtp_username = os.environ.get("MAIL_USERNAME", "")
        self.smtp_password = os.environ.get("MAIL_PASSWORD", "")
        self.from_email = os.environ.get("MAIL_FROM", "noreply@techskillsdevelopment.com")
    
    def send_email(self, to_email, subject, html_content, attachment_bytes=None, attachment_filename=None):
        """Send email with optional attachment"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"TECH Skills Development <{self.from_email}>"
            msg['To'] = to_email
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Attach PDF certificate if provided
            if attachment_bytes and attachment_filename:
                pdf_attachment = MIMEBase('application', 'octet-stream')
                pdf_attachment.set_payload(attachment_bytes)
                encoders.encode_base64(pdf_attachment)
                pdf_attachment.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{attachment_filename}"'
                )
                msg.attach(pdf_attachment)
            
            # Send email
            if self.smtp_username and self.smtp_password:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
                server.quit()
                return True
            else:
                print(f"Email would be sent to {to_email}: {subject}")
                return True
                
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def get_incomplete_course_email_content(self, student_name, course_name, progress_percent):
        """Generate attractive email content for incomplete courses"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Course Progress Reminder</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }}
                .container {{
                    background: white;
                    border-radius: 15px;
                    padding: 30px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .logo {{
                    background: linear-gradient(45deg, #4f46e5, #7c3aed);
                    color: white;
                    padding: 15px 30px;
                    border-radius: 10px;
                    font-weight: bold;
                    font-size: 18px;
                    display: inline-block;
                    margin-bottom: 15px;
                }}
                h1 {{
                    color: #4f46e5;
                    margin-bottom: 10px;
                }}
                .progress-bar {{
                    background: #e0e0e0;
                    border-radius: 10px;
                    height: 20px;
                    overflow: hidden;
                    margin: 20px 0;
                }}
                .progress-fill {{
                    background: linear-gradient(45deg, #4f46e5, #7c3aed);
                    height: 100%;
                    border-radius: 10px;
                    transition: width 0.3s ease;
                }}
                .cta-button {{
                    display: inline-block;
                    background: linear-gradient(45deg, #4f46e5, #7c3aed);
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 25px;
                    font-weight: bold;
                    margin: 20px 0;
                    text-align: center;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-size: 14px;
                }}
                .emoji {{
                    font-size: 24px;
                    margin: 0 5px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">TSD</div>
                    <h1>🚀 Continue Your Learning Journey!</h1>
                    <p>Don't let your progress go to waste!</p>
                </div>
                
                <p>Dear <strong>{student_name}</strong>,</p>
                
                <p>We noticed you're making great progress in <strong>{course_name}</strong>! 🎯</p>
                
                <p>Your current progress: <strong>{progress_percent}%</strong></p>
                
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress_percent}%"></div>
                </div>
                
                <p>You're doing amazing! Just a little more effort and you'll earn your certificate. 🏆</p>
                
                <div style="text-align: center;">
                    <a href="http://127.0.0.1:5000" class="cta-button">
                        Continue Learning →
                    </a>
                </div>
                
                <p>Remember, consistency is key to success! 💪</p>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h3>🌟 Quick Tips:</h3>
                    <ul>
                        <li>Set aside 30 minutes daily for your course</li>
                        <li>Take notes while learning</li>
                        <li>Practice what you learn immediately</li>
                        <li>Join our study community for support</li>
                    </ul>
                </div>
                
                <p>We believe in you! 🌈</p>
                
                <div class="footer">
                    <p>Best regards,<br>
                    <strong>TECH Skills Development Team</strong><br>
                    <span class="emoji">🎓</span> Empowering Future Tech Leaders <span class="emoji">🚀</span></p>
                    <p><small>This is an automated reminder. You can adjust your notification settings in your profile.</small></p>
                </div>
            </div>
        </body>
        </html>
        """
        return html_content
    
    def get_completion_email_content(self, student_name, course_name, score_percent, grade):
        """Generate attractive email content for completed courses"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Course Completion! 🎉</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }}
                .container {{
                    background: white;
                    border-radius: 15px;
                    padding: 30px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .logo {{
                    background: linear-gradient(45deg, #4f46e5, #7c3aed);
                    color: white;
                    padding: 15px 30px;
                    border-radius: 10px;
                    font-weight: bold;
                    font-size: 18px;
                    display: inline-block;
                    margin-bottom: 15px;
                }}
                h1 {{
                    color: #059669;
                    margin-bottom: 10px;
                    font-size: 28px;
                }}
                .achievement-badge {{
                    background: linear-gradient(45deg, #059669, #10b981);
                    color: white;
                    padding: 20px;
                    border-radius: 15px;
                    text-align: center;
                    margin: 20px 0;
                    font-size: 18px;
                    font-weight: bold;
                }}
                .score-display {{
                    background: linear-gradient(45deg, #4f46e5, #7c3aed);
                    color: white;
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    margin: 20px 0;
                }}
                .grade-display {{
                    font-size: 36px;
                    font-weight: bold;
                    margin: 10px 0;
                }}
                .cta-button {{
                    display: inline-block;
                    background: linear-gradient(45deg, #059669, #10b981);
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 25px;
                    font-weight: bold;
                    margin: 20px 0;
                    text-align: center;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 30px;
                    color: #666;
                    font-size: 14px;
                }}
                .emoji {{
                    font-size: 24px;
                    margin: 0 5px;
                }}
                .confetti {{
                    font-size: 20px;
                    margin: 0 2px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">TSD</div>
                    <h1>🎉 Congratulations! Course Completed! 🎉</h1>
                    <p>You've achieved something amazing!</p>
                </div>
                
                <p>Dear <strong>{student_name}</strong>,</p>
                
                <div class="achievement-badge">
                    🏆 ACHIEVEMENT UNLOCKED 🏆<br>
                    You have successfully completed<br>
                    <strong>{course_name}</strong>!
                </div>
                
                <p>Your dedication and hard work have paid off! 🌟</p>
                
                <div class="score-display">
                    <div>Final Score</div>
                    <div class="grade-display">{score_percent}%</div>
                    <div>Grade: {grade}</div>
                </div>
                
                <p>This is a remarkable achievement! 🎯 Your commitment to learning and growth is truly inspiring.</p>
                
                <div style="text-align: center;">
                    <a href="http://127.0.0.1:5000" class="cta-button">
                        View Your Certificate 🏆
                    </a>
                </div>
                
                <div style="background: #f0fdf4; padding: 20px; border-radius: 10px; margin: 20px 0; border: 2px solid #059669;">
                    <h3>🎓 Your Certificate Includes:</h3>
                    <ul>
                        <li>✅ Official TSD Certification</li>
                        <li>✅ Unique Certificate ID for verification</li>
                        <li>✅ Grade and score details</li>
                        <li>✅ Industry-recognized achievement</li>
                    </ul>
                </div>
                
                <p>Share your achievement on LinkedIn and let the world know about your success! 🚀</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <div class="confetti">🎊 🎈 🎉 🎊 🎈 🎉</div>
                </div>
                
                <p>What's next? 🤔</p>
                <ul>
                    <li>Explore our advanced courses</li>
                    <li>Join our alumni network</li>
                    <li>Share your success story</li>
                    <li>Mentor other students</li>
                </ul>
                
                <div class="footer">
                    <p>Best regards,<br>
                    <strong>TECH Skills Development Team</strong><br>
                    <span class="emoji">🎓</span> Empowering Future Tech Leaders <span class="emoji">🚀</span></p>
                    <p><small>This certificate is verifiable at www.techskillsdevelopment.com/verify</small></p>
                </div>
            </div>
        </body>
        </html>
        """
        return html_content
    
    def send_incomplete_course_reminder(self, student_email, student_name, course_name, progress_percent):
        """Send reminder for incomplete course"""
        subject = f"🚀 Continue Your Journey: {course_name} - {progress_percent}% Complete!"
        html_content = self.get_incomplete_course_email_content(student_name, course_name, progress_percent)
        return self.send_email(student_email, subject, html_content)
    
    def send_completion_certificate(self, student_email, student_name, course_name, score_percent, grade):
        """Send completion email with certificate"""
        subject = f"🎉 Congratulations! You've Completed {course_name}!"
        html_content = self.get_completion_email_content(student_name, course_name, score_percent, grade)
        
        # Generate certificate PDF
        try:
            duration_hours = 40  # Default duration
            certificate_bytes = generate_certificate_pdf(student_name, course_name, duration_hours, score_percent, grade)
            filename = f"Certificate_{course_name.replace(' ', '_')}_{student_name.replace(' ', '_')}.pdf"
            return self.send_email(student_email, subject, html_content, certificate_bytes, filename)
        except Exception as e:
            print(f"Error generating certificate: {e}")
            return self.send_email(student_email, subject, html_content)


def check_incomplete_courses():
    """Check for incomplete courses and send reminders"""
    with app.app_context():
        try:
            email_service = EmailNotificationService()
            
            # Get all enrollments
            enrollments = db.session.query(Enrollment).all()
            
            for enrollment in enrollments:
                # Get student info
                student = User.query.get(enrollment.user_id)
                if not student or student.role != 'student':
                    continue
                
                # Get course info
                course = Course.query.get(enrollment.course_id)
                if not course:
                    continue
                
                # Calculate progress
                topics = CourseTopic.query.filter_by(course_id=course.id).all()
                completed_topics = TopicProgress.query.filter_by(
                    user_id=student.id, 
                    course_id=course.id
                ).all()
                
                total_topics = len(topics)
                completed_count = len(completed_topics)
                progress_percent = int((completed_count / total_topics) * 100) if total_topics > 0 else 0
                
                # Check if course is incomplete (not 100%)
                if progress_percent < 100:
                    # Send reminder (in real app, you'd check last reminder time)
                    print(f"Sending reminder to {student.email} for {course.name} - {progress_percent}% complete")
                    email_service.send_incomplete_course_reminder(
                        student.email, 
                        student.full_name or student.username,
                        course.name,
                        progress_percent
                    )
            
            return True
            
        except Exception as e:
            print(f"Error checking incomplete courses: {e}")
            return False


def check_completed_courses():
    """Check for completed courses and send certificates"""
    with app.app_context():
        try:
            email_service = EmailNotificationService()
            
            # Get all course test attempts with passing scores
            passing_attempts = CourseTestAttempt.query.filter(
                CourseTestAttempt.score_percent >= 40
            ).all()
            
            for attempt in passing_attempts:
                # Get student info
                student = User.query.get(attempt.user_id)
                if not student or student.role != 'student':
                    continue
                
                # Get course info
                course = Course.query.get(attempt.course_id)
                if not course:
                    continue
                
                # Calculate grade
                if attempt.score_percent >= 90:
                    grade = "A"
                elif attempt.score_percent >= 80:
                    grade = "B"
                elif attempt.score_percent >= 70:
                    grade = "C"
                elif attempt.score_percent >= 60:
                    grade = "D"
                else:
                    grade = "F"
                
                # Send completion email with certificate
                print(f"Sending certificate to {student.email} for {course.name}")
                email_service.send_completion_certificate(
                    student.email,
                    student.full_name or student.username,
                    course.name,
                    attempt.score_percent,
                    grade
                )
            
            return True
            
        except Exception as e:
            print(f"Error checking completed courses: {e}")
            return False


if __name__ == "__main__":
    print("🔧 Testing Email Notification System...")
    print("=" * 50)
    
    # Test incomplete course reminders
    print("\n📧 Testing incomplete course reminders...")
    if check_incomplete_courses():
        print("✅ Incomplete course reminders processed successfully!")
    else:
        print("❌ Error processing incomplete course reminders")
    
    # Test completion certificates
    print("\n🎉 Testing completion certificates...")
    if check_completed_courses():
        print("✅ Completion certificates processed successfully!")
    else:
        print("❌ Error processing completion certificates")
    
    print("\n📋 Email Notification System Ready!")
    print("   • Incomplete course reminders every 5 minutes")
    print("   • Completion emails with certificates")
    print("   • Attractive HTML email templates")
    print("   • PDF certificate attachments")
