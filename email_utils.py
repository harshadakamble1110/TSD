"""Send alert emails via SMTP."""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config as app_config


def _smtp_configured():
    return bool(app_config.MAIL_SERVER and app_config.MAIL_USERNAME and app_config.MAIL_PASSWORD)


def send_email(to_email, subject, body_text):
    """Send a plain-text email. Returns True if sent, False if SMTP not configured or error."""
    if not _smtp_configured():
        return False
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = app_config.MAIL_FROM
        msg["To"] = to_email
        msg.attach(MIMEText(body_text, "plain"))
        with smtplib.SMTP(app_config.MAIL_SERVER, app_config.MAIL_PORT) as server:
            if app_config.MAIL_USE_TLS:
                server.starttls()
            server.login(app_config.MAIL_USERNAME, app_config.MAIL_PASSWORD)
            server.sendmail(app_config.MAIL_FROM, to_email, msg.as_string())
        return True
    except Exception:
        return False


# ---------- Alert message builders ----------

def email_enrolled_welcome(to_email, student_name, course_name):
    subject = "You're enrolled in " + course_name + " — TECH Skills Development"
    body = (
        "Hi " + (student_name or "there") + ",\n\n"
        "You have successfully enrolled in: " + course_name + ".\n\n"
        "Start learning now! Log in and open the course to begin with the first topic (Introduction).\n\n"
        "Best regards,\nTECH Skills Development"
    )
    return send_email(to_email, subject, body)


def email_enrolled_not_continued(to_email, student_name, course_name, days=1):
    subject = "Reminder: Start your course — " + course_name
    body = (
        "Hi " + (student_name or "there") + ",\n\n"
        "You enrolled in " + course_name + " but haven't started yet.\n\n"
        "Don't wait — open the course and complete the first topic to unlock the rest.\n\n"
        "Best regards,\nTECH Skills Development"
    )
    return send_email(to_email, subject, body)


def email_partial_progress(to_email, student_name, course_name, completed_count, total_topics):
    subject = "You're making progress — " + course_name
    body = (
        "Hi " + (student_name or "there") + ",\n\n"
        "You've completed " + str(completed_count) + " of " + str(total_topics) + " topics in " + course_name + ".\n\n"
        "Keep going! Complete the next topic to move forward.\n\n"
        "Best regards,\nTECH Skills Development"
    )
    return send_email(to_email, subject, body)


def email_quiz_not_completed(to_email, student_name, topic_name):
    subject = "Reminder: Complete your quiz — " + topic_name
    body = (
        "Hi " + (student_name or "there") + ",\n\n"
        "You started the quiz for \"" + topic_name + "\" but didn't finish it.\n\n"
        "Complete the quiz to unlock the next topic.\n\n"
        "Best regards,\nTECH Skills Development"
    )
    return send_email(to_email, subject, body)


def email_test_not_completed(to_email, student_name, course_name):
    subject = "Reminder: Complete your course test — " + course_name
    body = (
        "Hi " + (student_name or "there") + ",\n\n"
        "You started the final test for " + course_name + " but didn't finish it.\n\n"
        "Complete the test to see your score and review your answers.\n\n"
        "Best regards,\nTECH Skills Development"
    )
    return send_email(to_email, subject, body)


def email_pending_work_summary(to_email, student_name, pending_list):
    """pending_list: list of strings like ['Course A: 2 topics left', 'Course B: Quiz incomplete']"""
    subject = "You have pending work — TECH Skills Development"
    body = (
        "Hi " + (student_name or "there") + ",\n\n"
        "Here's a quick reminder of your pending work:\n\n"
        + "\n".join("• " + p for p in pending_list) + "\n\n"
        "Log in to continue learning.\n\n"
        "Best regards,\nTECH Skills Development"
    )
    return send_email(to_email, subject, body)
