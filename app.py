
import os
import json
import io
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps

import config as app_config
from email_utils import email_enrolled_welcome
from models import (
    db, User, StudentDetail, Category, Course, CourseTopic,
    Enrollment, TopicProgress, TopicQuizAttempt, CourseTestAttempt, Complaint
)
from certificate_generator import generate_certificate_pdf
import uuid
import random
import string

app = Flask(__name__)

# Video upload configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads', 'videos')
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'webm', 'ogg', 'mov', 'avi', 'mkv'}
MAX_VIDEO_SIZE = 500 * 1024 * 1024  # 500MB max file size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_video_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS


def generate_unique_student_id():
    """Generate a unique student ID in format TS + 8 random alphanumeric characters."""
    max_attempts = 100  # Prevent infinite loop
    for _ in range(max_attempts):
        # Generate TS + 8 random characters (alphanumeric)
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        student_id = f"TS{random_part}"
        # Check if this ID already exists
        try:
            if not User.query.filter_by(student_id=student_id).first():
                return student_id
        except Exception:
            # If database query fails, return the generated ID anyway
            # The unique constraint will catch duplicates
            return student_id
    # Fallback: use timestamp + random if max attempts reached
    return f"TS{int(datetime.now().timestamp())}{''.join(random.choices(string.digits, k=4))}"
app.config["SECRET_KEY"] = app_config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = app_config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = app_config.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."


@login_manager.user_loader
def load_user(user_id):
    if user_id is None:
        return None
    try:
        return User.query.get(int(user_id))
    except (ValueError, TypeError):
        return None


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            flash("Admin access required.", "error")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


@app.route("/")
def index():
    if current_user.is_authenticated:
        if current_user.role == "admin":
            return redirect(url_for("admin_dashboard"))
        return redirect(url_for("home"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username == app_config.ADMIN_USERNAME and password == app_config.ADMIN_PASSWORD:
            admin = User.query.filter_by(username=app_config.ADMIN_USERNAME).first()
            if not admin:
                admin = User(username=app_config.ADMIN_USERNAME, email="admin@techskills.com", role="admin")
                admin.set_password(app_config.ADMIN_PASSWORD)
                db.session.add(admin)
                db.session.commit()
            login_user(admin, remember=True)
            return redirect(url_for("admin_dashboard"))
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password) and user.role == "student":
            login_user(user, remember=True)
            return redirect(url_for("home"))
        flash("Invalid username or password.", "error")
    return render_template("student/login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        full_name = request.form.get("full_name", "").strip()
        if not username or not email or not password:
            flash("Username, email and password are required.", "error")
            return render_template("student/register.html")
        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "error")
            return render_template("student/register.html")
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return render_template("student/register.html")
        user = User(username=username, email=email, full_name=full_name, role="student")
        user.student_id = generate_unique_student_id()
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("student/register.html")


@app.route("/student-details", methods=["GET", "POST"])
@login_required
def student_details():
    if current_user.role != "student":
        return redirect(url_for("home"))
    detail = StudentDetail.query.filter_by(user_id=current_user.id).first()
    if request.method == "POST":
        if not detail:
            detail = StudentDetail(user_id=current_user.id)
            db.session.add(detail)
        email = request.form.get("email", "").strip()
        if email:
            current_user.email = email
        current_user.full_name = request.form.get("full_name", "").strip()
        detail.phone = request.form.get("phone", "").strip()
        db.session.commit()
        flash("Details saved successfully.", "success")
        return redirect(url_for("student_details"))
    return render_template("student/student_details.html", detail=detail)


@app.route("/home")
@login_required
def home():
    if current_user.role != "student":
        return redirect(url_for("admin_dashboard"))
    categories = Category.query.order_by(Category.id).all()
    search_query = request.args.get("q", "").strip()
    courses = []
    if search_query:
        courses = Course.query.filter(Course.name.ilike(f"%{search_query}%")).all()
    return render_template("student/home.html", categories=categories, courses=courses, search_query=search_query)


@app.route("/search")
@login_required
def search():
    if current_user.role != "student":
        return redirect(url_for("admin_dashboard"))
    query = request.args.get("q", "").strip()
    courses = []
    if query:
        courses = Course.query.filter(Course.name.ilike(f"%{query}%")).all()
    return render_template("student/search_results.html", courses=courses, query=query)


@app.route("/courses/<category_slug>")
@login_required
def courses_list(category_slug):
    if current_user.role != "student":
        return redirect(url_for("admin_dashboard"))
    cat = Category.query.filter_by(slug=category_slug).first_or_404()
    courses = Course.query.filter_by(category_id=cat.id).order_by(Course.id).all()
    return render_template("student/courses_list.html", category=cat, courses=courses)


@app.route("/course/<int:course_id>")
@login_required
def course_detail(course_id):
    if current_user.role != "student":
        return redirect(url_for("admin_dashboard"))
    course = Course.query.get_or_404(course_id)
    enrolled = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first() is not None
    return render_template("student/course_detail.html", course=course, enrolled=enrolled)


def _is_profile_complete():
    """Profile complete = full_name and phone (for certificate)."""
    if not current_user.full_name or not current_user.full_name.strip():
        return False
    detail = StudentDetail.query.filter_by(user_id=current_user.id).first()
    if not detail:
        return False
    return bool(detail.phone and detail.phone.strip())


@app.route("/api/profile-complete")
@login_required
def api_profile_complete():
    if current_user.role != "student":
        return jsonify({"profile_complete": False})
    return jsonify({"profile_complete": _is_profile_complete()})


@app.route("/enroll/<int:course_id>", methods=["POST"])
@login_required
def enroll(course_id):
    if current_user.role != "student":
        return jsonify({"ok": False})
    if not _is_profile_complete():
        return jsonify({"ok": False, "profile_complete": False})
    course = Course.query.get_or_404(course_id)
    if Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first():
        return jsonify({"ok": True, "already": True})
    e = Enrollment(user_id=current_user.id, course_id=course_id)
    db.session.add(e)
    db.session.commit()
    try:
        email_enrolled_welcome(
            current_user.email,
            current_user.full_name,
            course.name
        )
    except Exception:
        pass
    return jsonify({"ok": True})


@app.route("/my-course/<int:course_id>")
@login_required
def enrolled_course(course_id):
    if current_user.role != "student":
        return redirect(url_for("admin_dashboard"))
    course = Course.query.get_or_404(course_id)
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    if not enrollment:
        flash("You are not enrolled in this course.", "error")
        return redirect(url_for("course_detail", course_id=course_id))
    topics = CourseTopic.query.filter_by(course_id=course_id).order_by(CourseTopic.order).all()
    completed_ids = {
        p.topic_id for p in TopicProgress.query.filter_by(
            user_id=current_user.id, course_id=course_id
        ).all()
    }
    return render_template(
        "student/enrolled_course.html",
        course=course,
        topics=topics,
        completed_ids=completed_ids
    )


def _ensure_enrolled_and_unlocked(user_id, topic):
    enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=topic.course_id).first()
    if not enrollment:
        return redirect(url_for("course_detail", course_id=topic.course_id))
    topics = CourseTopic.query.filter_by(course_id=topic.course_id).order_by(CourseTopic.order).all()
    completed_ids = {
        p.topic_id for p in TopicProgress.query.filter_by(
            user_id=user_id, course_id=topic.course_id
        ).all()
    }
    idx = next((i for i, t in enumerate(topics) if t.id == topic.id), None)
    unlocked = idx == 0 or (idx is not None and (topics[idx - 1].id in completed_ids))
    if not unlocked:
        flash("Complete the previous topic first.", "error")
        return redirect(url_for("enrolled_course", course_id=topic.course_id))
    return None


@app.route("/topic/<int:topic_id>")
@login_required
def topic_view(topic_id):
    """Redirect to enrolled course - topic view is handled within enrolled course page."""
    topic = CourseTopic.query.get_or_404(topic_id)
    return redirect(url_for("enrolled_course", course_id=topic.course_id))


@app.route("/topic/<int:topic_id>/video")
@login_required
def topic_video(topic_id):
    topic = CourseTopic.query.get_or_404(topic_id)
    r = _ensure_enrolled_and_unlocked(current_user.id, topic)
    if r is not None:
        return r
    # Get next topic for "Next" button
    topics_ordered = CourseTopic.query.filter_by(course_id=topic.course_id).order_by(CourseTopic.order).all()
    idx = next((i for i, t in enumerate(topics_ordered) if t.id == topic.id), None)
    next_topic = None
    if idx is not None and idx + 1 < len(topics_ordered):
        next_topic = topics_ordered[idx + 1]
    return render_template("student/topic_video.html", topic=topic, course=topic.course, next_topic=next_topic)


@app.route("/topic/<int:topic_id>/notes")
@login_required
def topic_notes(topic_id):
    topic = CourseTopic.query.get_or_404(topic_id)
    r = _ensure_enrolled_and_unlocked(current_user.id, topic)
    if r is not None:
        return r
    return render_template("student/topic_notes.html", topic=topic, course=topic.course)


@app.route("/topic/<int:topic_id>/quiz", methods=["GET", "POST"])
@login_required
def topic_quiz(topic_id):
    topic = CourseTopic.query.get_or_404(topic_id)
    r = _ensure_enrolled_and_unlocked(current_user.id, topic)
    if r is not None:
        return r
    # Allow reattempt if score < 40%
    existing = TopicQuizAttempt.query.filter_by(user_id=current_user.id, topic_id=topic_id).first()
    if existing and request.method == "GET" and existing.score_percent >= 40:
        return redirect(url_for("topic_quiz_result", topic_id=topic_id))
    questions = []
    if topic.quiz_questions:
        try:
            questions = json.loads(topic.quiz_questions)
        except Exception:
            pass
    if request.method == "POST":
        data = request.get_json() or {}
        answers = data.get("answers", [])
        correct = 0
        results = []
        for i, q in enumerate(questions):
            sel = answers[i] if i < len(answers) else None
            cidx = q.get("correct_index", 0)
            is_correct = sel is not None and int(sel) == int(cidx)
            if is_correct:
                correct += 1
            results.append({
                "question": q.get("question", ""),
                "options": q.get("options", []),
                "correct_index": cidx,
                "selected_index": sel,
                "correct": is_correct
            })
        total = len(questions) or 1
        score_percent = round(100 * correct / total, 1)
        attempt = TopicQuizAttempt(
            user_id=current_user.id,
            topic_id=topic_id,
            score_percent=score_percent,
            answers_json=json.dumps(results)
        )
        # Delete old attempt if reattempting
        if existing:
            db.session.delete(existing)
        db.session.add(attempt)
        # Unlock next topic only if score >= 40%
        if score_percent >= 40:
            prog = TopicProgress(
                user_id=current_user.id,
                course_id=topic.course_id,
                topic_id=topic_id
            )
            db.session.add(prog)
        db.session.commit()
        return jsonify({
            "score_percent": score_percent,
            "total": total,
            "correct": correct,
            "results": results
        })
    return render_template(
        "student/topic_quiz.html",
        topic=topic,
        course=topic.course,
        questions=questions
    )


@app.route("/course/<int:course_id>/test", methods=["GET", "POST"])
@login_required
def course_test(course_id):
    course = Course.query.get_or_404(course_id)
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    if not enrollment:
        return redirect(url_for("course_detail", course_id=course_id))
    # One attempt only: if already attempted, show result
    existing_test = CourseTestAttempt.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    if existing_test and request.method == "GET":
        return redirect(url_for("course_test_result", course_id=course_id))
    test_topic = CourseTopic.query.filter_by(
        course_id=course_id
    ).filter(CourseTopic.course_test_questions.isnot(None)).first()
    if not test_topic or not test_topic.course_test_questions:
        flash("Test not available.", "error")
        return redirect(url_for("enrolled_course", course_id=course_id))
    questions = []
    try:
        questions = json.loads(test_topic.course_test_questions)
    except Exception:
        pass
    if request.method == "POST":
        data = request.get_json() or {}
        answers = data.get("answers", [])
        correct = 0
        results = []
        for i, q in enumerate(questions):
            sel = answers[i] if i < len(answers) else None
            cidx = q.get("correct_index", 0)
            is_correct = sel is not None and int(sel) == int(cidx)
            if is_correct:
                correct += 1
            results.append({
                "question": q.get("question", ""),
                "options": q.get("options", []),
                "correct_index": cidx,
                "selected_index": sel,
                "correct": is_correct
            })
        total = len(questions) or 1
        score_percent = round(100 * correct / total, 1)
        attempt = CourseTestAttempt(
            user_id=current_user.id,
            course_id=course_id,
            score_percent=score_percent,
            answers_json=json.dumps(results)
        )
        db.session.add(attempt)
        prog = TopicProgress(
            user_id=current_user.id,
            course_id=course_id,
            topic_id=test_topic.id
        )
        db.session.add(prog)
        db.session.commit()
        return jsonify({
            "score_percent": score_percent,
            "total": total,
            "correct": correct,
            "results": results
        })
    return render_template(
        "student/course_test.html",
        course=course,
        questions=questions
    )


def _grade_from_percent(percent):
    if percent >= 90:
        return "A+"
    if percent >= 80:
        return "A"
    if percent >= 70:
        return "B+"
    if percent >= 60:
        return "B"
    if percent >= 50:
        return "C"
    return "F"


@app.route("/topic/<int:topic_id>/quiz/result")
@login_required
def topic_quiz_result(topic_id):
    topic = CourseTopic.query.get_or_404(topic_id)
    attempt = TopicQuizAttempt.query.filter_by(
        user_id=current_user.id, topic_id=topic_id
    ).order_by(TopicQuizAttempt.attempted_at.desc()).first()
    if not attempt:
        return redirect(url_for("topic_quiz", topic_id=topic_id))
    results = []
    if attempt.answers_json:
        try:
            results = json.loads(attempt.answers_json)
        except Exception:
            pass
    # Next: next topic, or course test, or certificate
    topics_ordered = CourseTopic.query.filter_by(course_id=topic.course_id).order_by(CourseTopic.order).all()
    idx = next((i for i, t in enumerate(topics_ordered) if t.id == topic.id), None)
    next_topic = None
    next_step = None  # 'course_test' or 'certificate'
    if idx is not None and idx + 1 < len(topics_ordered):
        next_topic = topics_ordered[idx + 1]
        if next_topic.course_test_questions:
            next_step = "course_test"
    can_reattempt = attempt.score_percent < 40
    return render_template(
        "student/quiz_result.html",
        topic=topic,
        course=topic.course,
        score_percent=attempt.score_percent,
        results=results,
        is_course_test=False,
        next_topic=next_topic,
        next_step=next_step,
        can_reattempt=can_reattempt
    )


@app.route("/course/<int:course_id>/test/result")
@login_required
def course_test_result(course_id):
    course = Course.query.get_or_404(course_id)
    attempt = CourseTestAttempt.query.filter_by(
        user_id=current_user.id, course_id=course_id
    ).order_by(CourseTestAttempt.attempted_at.desc()).first()
    if not attempt:
        return redirect(url_for("course_test", course_id=course_id))
    results = []
    if attempt.answers_json:
        try:
            results = json.loads(attempt.answers_json)
        except Exception:
            pass
    return render_template(
        "student/quiz_result.html",
        topic=None,
        course=course,
        score_percent=attempt.score_percent,
        results=results,
        is_course_test=True,
        next_topic=None,
        next_step="certificate"
    )


@app.route("/course/<int:course_id>/certificate")
@login_required
def certificate(course_id):
    course = Course.query.get_or_404(course_id)
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    if not enrollment:
        return redirect(url_for("course_detail", course_id=course_id))
    # Check if test topic is completed
    test_topic = CourseTopic.query.filter_by(course_id=course_id).filter(
        CourseTopic.course_test_questions.isnot(None)
    ).first()
    if not test_topic:
        flash("Course test not available.", "error")
        return redirect(url_for("enrolled_course", course_id=course_id))
    test_completed = TopicProgress.query.filter_by(
        user_id=current_user.id, course_id=course_id, topic_id=test_topic.id
    ).first()
    if not test_completed:
        flash("Complete the course test to view your certificate.", "error")
        return redirect(url_for("enrolled_course", course_id=course_id))
    attempt = CourseTestAttempt.query.filter_by(
        user_id=current_user.id, course_id=course_id
    ).order_by(CourseTestAttempt.attempted_at.desc()).first()
    if not attempt:
        flash("Complete the course test to view your certificate.", "error")
        return redirect(url_for("enrolled_course", course_id=course_id))
    # Mark certificate topic as completed if not already
    cert_topic = CourseTopic.query.filter_by(course_id=course_id).filter(
        CourseTopic.title.ilike("%certificate%")
    ).first()
    if cert_topic:
        cert_progress = TopicProgress.query.filter_by(
            user_id=current_user.id, course_id=course_id, topic_id=cert_topic.id
        ).first()
        if not cert_progress:
            cert_prog = TopicProgress(user_id=current_user.id, course_id=course_id, topic_id=cert_topic.id)
            db.session.add(cert_prog)
            db.session.commit()
    grade = _grade_from_percent(attempt.score_percent)
    return render_template(
        "student/certificate.html",
        course=course,
        score_percent=attempt.score_percent,
        grade=grade
    )


@app.route("/course/<int:course_id>/certificate/download")
@login_required
def certificate_download(course_id):
    course = Course.query.get_or_404(course_id)
    enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first()
    if not enrollment:
        return redirect(url_for("course_detail", course_id=course_id))
    test_topic = CourseTopic.query.filter_by(course_id=course_id).filter(
        CourseTopic.course_test_questions.isnot(None)
    ).first()
    if not test_topic:
        flash("Course test not available.", "error")
        return redirect(url_for("enrolled_course", course_id=course_id))
    test_completed = TopicProgress.query.filter_by(
        user_id=current_user.id, course_id=course_id, topic_id=test_topic.id
    ).first()
    if not test_completed:
        flash("Complete the course test to download certificate.", "error")
        return redirect(url_for("enrolled_course", course_id=course_id))
    attempt = CourseTestAttempt.query.filter_by(
        user_id=current_user.id, course_id=course_id
    ).order_by(CourseTestAttempt.attempted_at.desc()).first()
    if not attempt:
        flash("Complete the course test to download certificate.", "error")
        return redirect(url_for("enrolled_course", course_id=course_id))
    grade = _grade_from_percent(attempt.score_percent)
    student_name = current_user.full_name if current_user.full_name else current_user.username
    if generate_certificate_pdf is None:
        flash("PDF download requires 'reportlab'. Install with: pip install reportlab", "error")
        return redirect(url_for("certificate", course_id=course_id))
    duration_hours = course.duration_weeks
    pdf_bytes = generate_certificate_pdf(student_name, course.name, duration_hours, attempt.score_percent, grade)
    filename = f"Certificate_{course.slug}_{current_user.student_id or current_user.id}.pdf"
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if current_user.role != "student":
        return redirect(url_for("admin_dashboard"))
    if request.method == "POST":
        action = request.form.get("action")
        if action == "profile":
            current_user.full_name = request.form.get("full_name", "").strip()
            db.session.commit()
            flash("Profile updated.", "success")
        elif action == "password":
            cur = request.form.get("current_password", "")
            new = request.form.get("new_password", "")
            if not current_user.check_password(cur):
                flash("Current password is wrong.", "error")
            elif len(new) < 6:
                flash("New password must be at least 6 characters.", "error")
            else:
                current_user.set_password(new)
                db.session.commit()
                flash("Password updated.", "success")
        return redirect(url_for("settings"))
    # Show student's complaints and settings
    complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    return render_template("student/settings.html", complaints=complaints)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ---------- Footer Pages ----------
@app.route("/about-us")
def about_us():
    return render_template("student/about_us.html")


@app.route("/refer-earn")
@login_required
def refer_earn():
    if current_user.role != "student":
        return redirect(url_for("admin_dashboard"))
    return render_template("student/refer_earn.html")


@app.route("/downloads")
@login_required
def downloads():
    if current_user.role != "student":
        return redirect(url_for("admin_dashboard"))
    return render_template("student/downloads.html")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated and current_user.role == "admin":
        return redirect(url_for("admin_dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if username == app_config.ADMIN_USERNAME and password == app_config.ADMIN_PASSWORD:
            admin = User.query.filter_by(username=app_config.ADMIN_USERNAME).first()
            if not admin:
                admin = User(username=app_config.ADMIN_USERNAME, email="admin@techskills.com", role="admin")
                admin.set_password(app_config.ADMIN_PASSWORD)
                db.session.add(admin)
                db.session.commit()
            login_user(admin)
            return redirect(url_for("admin_dashboard"))
        flash("Invalid admin credentials.", "error")
    return render_template("admin/admin_login.html")


@app.route("/admin/dashboard")
@login_required
@admin_required
def admin_dashboard():
    total_students = User.query.filter_by(role="student").count()
    total_courses = Course.query.count()
    total_enrollments = Enrollment.query.count()
    categories = Category.query.count()
    return render_template(
        "admin/admin_dashboard.html",
        total_students=total_students,
        total_courses=total_courses,
        total_enrollments=total_enrollments,
        total_categories=categories
    )


@app.route("/admin/dashboard/stats")
@login_required
@admin_required
def admin_dashboard_stats():
    total_students = User.query.filter_by(role="student").count()
    total_courses = Course.query.count()
    total_enrollments = Enrollment.query.count()
    categories = Category.query.count()
    pending_complaints = Complaint.query.filter_by(status="pending").count()
    return render_template(
        "admin/admin_stats.html",
        total_students=total_students,
        total_courses=total_courses,
        total_enrollments=total_enrollments,
        total_categories=categories,
        pending_complaints=pending_complaints
    )


@app.route("/admin/logout")
@login_required
@admin_required
def admin_logout():
    logout_user()
    return redirect(url_for("admin_login"))


# ---------- Complaints ----------
@app.route("/complaint", methods=["GET", "POST"])
def complaint():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()
        if not name or not email or not subject or not message:
            flash("All fields are required.", "error")
            return render_template("student/complaint.html")
        user_id = current_user.id if current_user.is_authenticated else None
        complaint = Complaint(user_id=user_id, name=name, email=email, subject=subject, message=message)
        db.session.add(complaint)
        db.session.commit()
        flash("Complaint submitted successfully. We'll get back to you soon.", "success")
        next_url = request.form.get("next")
        if next_url:
            return redirect(next_url)
        return redirect(url_for("complaint"))
    return render_template("student/complaint.html")


@app.route("/admin/complaints")
@login_required
@admin_required
def admin_complaints():
    complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    return render_template("admin/admin_complaints.html", complaints=complaints)


@app.route("/admin/complaints/<int:complaint_id>/resolve", methods=["POST"])
@login_required
@admin_required
def admin_complaint_resolve(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    complaint.status = "resolved"
    db.session.commit()
    flash("Complaint marked as resolved.", "success")
    return redirect(url_for("admin_complaints"))


# ---------- Admin Student Data ----------
@app.route("/admin/students")
@login_required
@admin_required
def admin_students():
    search_query = request.args.get("q", "").strip()
    status_filter = request.args.get("status", "")  # pending, completed, all
    q = User.query.filter_by(role="student")
    if search_query:
        q = q.filter(
            (User.full_name.ilike(f"%{search_query}%")) |
            (User.student_id.ilike(f"%{search_query}%")) |
            (User.username.ilike(f"%{search_query}%"))
        )
    students = q.order_by(User.created_at.desc()).all()
    
    # Calculate enrollment status for each student
    student_data = []
    for student in students:
        enrollments = Enrollment.query.filter_by(user_id=student.id).all()
        courses_data = []
        for enr in enrollments:
            course = enr.course
            topics = CourseTopic.query.filter_by(course_id=course.id).order_by(CourseTopic.order).all()
            completed_topics = TopicProgress.query.filter_by(user_id=student.id, course_id=course.id).all()
            completed_ids = {t.topic_id for t in completed_topics}
            total_topics = len(topics)
            completed_count = len(completed_ids)
            status = "completed" if completed_count == total_topics and total_topics > 0 else "pending"
            courses_data.append({
                "course": course,
                "status": status,
                "progress": f"{completed_count}/{total_topics}"
            })
        
        # Filter by status if requested
        if status_filter == "pending":
            courses_data = [c for c in courses_data if c["status"] == "pending"]
        elif status_filter == "completed":
            courses_data = [c for c in courses_data if c["status"] == "completed"]
        
        if not status_filter or courses_data:
            student_data.append({
                "student": student,
                "courses": courses_data,
                "detail": StudentDetail.query.filter_by(user_id=student.id).first()
            })
    
    return render_template("admin/admin_students.html", student_data=student_data, search_query=search_query, status_filter=status_filter)


def _slugify(s):
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s.strip().lower()).strip("-") or "slug"


# ---------- Admin: Manage Content (single page with 5 options) ----------
@app.route("/admin/manage-content")
@login_required
@admin_required
def admin_manage_content():
    return render_template("admin/admin_manage_content.html")


# ---------- Admin: Categories (drill-down: Manage Content → Categories) ----------
@app.route("/admin/manage/categories")
@login_required
@admin_required
def admin_manage_categories():
    categories = Category.query.order_by(Category.id).all()
    return render_template("admin/admin_manage_categories.html", categories=categories)


# ---------- Admin: Courses (drill-down: Manage Content → Courses → categories → category → courses) ----------
@app.route("/admin/manage/courses")
@login_required
@admin_required
def admin_manage_courses():
    categories = Category.query.order_by(Category.id).all()
    return render_template("admin/admin_manage_courses_categories.html", categories=categories)


@app.route("/admin/manage/courses/<int:cat_id>")
@login_required
@admin_required
def admin_manage_courses_category(cat_id):
    cat = Category.query.get_or_404(cat_id)
    courses = Course.query.filter_by(category_id=cat_id).order_by(Course.id).all()
    return render_template("admin/admin_manage_courses_list.html", category=cat, courses=courses)


# ---------- Admin: Topics (drill-down: categories → category → courses → course → topics) ----------
@app.route("/admin/manage/topics")
@login_required
@admin_required
def admin_manage_topics():
    categories = Category.query.order_by(Category.id).all()
    return render_template("admin/admin_manage_topics_categories.html", categories=categories)


@app.route("/admin/manage/topics/<int:cat_id>")
@login_required
@admin_required
def admin_manage_topics_courses(cat_id):
    cat = Category.query.get_or_404(cat_id)
    courses = Course.query.filter_by(category_id=cat_id).order_by(Course.id).all()
    return render_template("admin/admin_manage_topics_courses.html", category=cat, courses=courses)


@app.route("/admin/manage/topics/<int:cat_id>/<int:course_id>")
@login_required
@admin_required
def admin_manage_topics_list(cat_id, course_id):
    cat = Category.query.get_or_404(cat_id)
    course = Course.query.get_or_404(course_id)
    if course.category_id != cat_id:
        return redirect(url_for("admin_manage_topics"))
    topics = CourseTopic.query.filter_by(course_id=course_id).order_by(CourseTopic.order).all()
    return render_template("admin/admin_manage_topics_list.html", category=cat, course=course, topics=topics)


# ---------- Admin: Quiz Questions (drill-down: categories → category → courses → course → topics → topic) ----------
@app.route("/admin/manage/quiz-questions")
@login_required
@admin_required
def admin_manage_quiz():
    categories = Category.query.order_by(Category.id).all()
    return render_template("admin/admin_manage_quiz_categories.html", categories=categories)


@app.route("/admin/manage/quiz-questions/<int:cat_id>")
@login_required
@admin_required
def admin_manage_quiz_courses(cat_id):
    cat = Category.query.get_or_404(cat_id)
    courses = Course.query.filter_by(category_id=cat_id).order_by(Course.id).all()
    return render_template("admin/admin_manage_quiz_courses.html", category=cat, courses=courses)


@app.route("/admin/manage/quiz-questions/<int:cat_id>/<int:course_id>")
@login_required
@admin_required
def admin_manage_quiz_topics(cat_id, course_id):
    cat = Category.query.get_or_404(cat_id)
    course = Course.query.get_or_404(course_id)
    if course.category_id != cat_id:
        return redirect(url_for("admin_manage_quiz"))
    topics = CourseTopic.query.filter_by(course_id=course_id).order_by(CourseTopic.order).all()
    return render_template("admin/admin_manage_quiz_topics.html", category=cat, course=course, topics=topics)


@app.route("/admin/manage/quiz-questions/<int:cat_id>/<int:course_id>/<int:topic_id>")
@login_required
@admin_required
def admin_manage_quiz_questions(cat_id, course_id, topic_id):
    cat = Category.query.get_or_404(cat_id)
    course = Course.query.get_or_404(course_id)
    topic = CourseTopic.query.get_or_404(topic_id)
    if topic.course_id != course_id or course.category_id != cat_id:
        return redirect(url_for("admin_manage_quiz"))
    questions = []
    if topic.quiz_questions:
        try:
            questions = json.loads(topic.quiz_questions)
        except Exception:
            pass
    return render_template("admin/admin_manage_quiz_questions.html", category=cat, course=course, topic=topic, questions=questions)


# ---------- Admin: Test Questions (drill-down: categories → category → courses → course) ----------
@app.route("/admin/manage/test-questions")
@login_required
@admin_required
def admin_manage_test():
    categories = Category.query.order_by(Category.id).all()
    return render_template("admin/admin_manage_test_categories.html", categories=categories)


@app.route("/admin/manage/test-questions/<int:cat_id>")
@login_required
@admin_required
def admin_manage_test_courses(cat_id):
    cat = Category.query.get_or_404(cat_id)
    courses = Course.query.filter_by(category_id=cat_id).order_by(Course.id).all()
    return render_template("admin/admin_manage_test_courses.html", category=cat, courses=courses)


@app.route("/admin/manage/test-questions/<int:cat_id>/<int:course_id>")
@login_required
@admin_required
def admin_manage_test_questions(cat_id, course_id):
    cat = Category.query.get_or_404(cat_id)
    course = Course.query.get_or_404(course_id)
    if course.category_id != cat_id:
        return redirect(url_for("admin_manage_test"))
    test_topic = CourseTopic.query.filter_by(course_id=course_id).filter(CourseTopic.course_test_questions.isnot(None)).first()
    questions = []
    if test_topic and test_topic.course_test_questions:
        try:
            questions = json.loads(test_topic.course_test_questions)
        except Exception:
            pass
    return render_template("admin/admin_manage_test_questions.html", category=cat, course=course, test_topic=test_topic, questions=questions)


# ---------- Admin: Categories (direct list - used from Manage Content) ----------
@app.route("/admin/categories")
@login_required
@admin_required
def admin_categories():
    categories = Category.query.order_by(Category.id).all()
    return render_template("admin/admin_categories.html", categories=categories)


@app.route("/admin/categories/add", methods=["GET", "POST"])
@login_required
@admin_required
def admin_category_add():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        slug = request.form.get("slug", "").strip() or _slugify(name)
        desc = request.form.get("description", "").strip()
        icon = request.form.get("icon", "").strip()
        if not name:
            flash("Name is required.", "error")
            return render_template("admin/admin_category_form.html", category=None)
        if Category.query.filter_by(slug=slug).first():
            flash("Slug already exists.", "error")
            return render_template("admin/admin_category_form.html", category=None)
        c = Category(name=name, slug=slug, description=desc, icon=icon)
        db.session.add(c)
        db.session.commit()
        flash("Category added.", "success")
        return redirect(url_for("admin_categories"))
    return render_template("admin/admin_category_form.html", category=None)


@app.route("/admin/categories/<int:cat_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def admin_category_edit(cat_id):
    cat = Category.query.get_or_404(cat_id)
    if request.method == "POST":
        cat.name = request.form.get("name", "").strip()
        cat.slug = request.form.get("slug", "").strip() or _slugify(cat.name)
        cat.description = request.form.get("description", "").strip()
        cat.icon = request.form.get("icon", "").strip()
        db.session.commit()
        flash("Category updated.", "success")
        return redirect(url_for("admin_categories"))
    return render_template("admin/admin_category_form.html", category=cat)


@app.route("/admin/categories/<int:cat_id>/delete", methods=["POST"])
@login_required
@admin_required
def admin_category_delete(cat_id):
    cat = Category.query.get_or_404(cat_id)
    db.session.delete(cat)
    db.session.commit()
    flash("Category deleted.", "success")
    return redirect(url_for("admin_categories"))


# ---------- Admin: Courses ----------
@app.route("/admin/courses")
@login_required
@admin_required
def admin_courses():
    category_id = request.args.get("category_id", type=int)
    q = Course.query
    if category_id:
        q = q.filter_by(category_id=category_id)
    courses = q.order_by(Course.id).all()
    categories = Category.query.order_by(Category.id).all()
    return render_template("admin/admin_courses.html", courses=courses, categories=categories, selected_category_id=category_id)


@app.route("/admin/courses/add", methods=["GET", "POST"])
@login_required
@admin_required
def admin_course_add():
    categories = Category.query.order_by(Category.id).all()
    if request.method == "POST":
        category_id = request.form.get("category_id", type=int)
        name = request.form.get("name", "").strip()
        slug = request.form.get("slug", "").strip() or _slugify(name)
        desc = request.form.get("description", "").strip()
        duration = request.form.get("duration_weeks", type=int) or 4
        syllabus = request.form.get("syllabus_text", "").strip()
        if not name or not category_id:
            flash("Name and category are required.", "error")
            return render_template("admin/admin_course_form.html", course=None, categories=categories)
        c = Course(category_id=category_id, name=name, slug=slug, description=desc, duration_weeks=duration, syllabus_text=syllabus)
        db.session.add(c)
        db.session.commit()
        flash("Course added.", "success")
        return redirect(url_for("admin_courses"))
    selected_category_id = request.args.get("category_id", type=int)
    return render_template("admin/admin_course_form.html", course=None, categories=categories, selected_category_id=selected_category_id)


@app.route("/admin/courses/<int:course_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def admin_course_edit(course_id):
    course = Course.query.get_or_404(course_id)
    categories = Category.query.order_by(Category.id).all()
    if request.method == "POST":
        course.category_id = request.form.get("category_id", type=int) or course.category_id
        course.name = request.form.get("name", "").strip() or course.name
        course.slug = request.form.get("slug", "").strip() or _slugify(course.name)
        course.description = request.form.get("description", "").strip()
        course.duration_weeks = request.form.get("duration_weeks", type=int) or 4
        course.syllabus_text = request.form.get("syllabus_text", "").strip()
        db.session.commit()
        flash("Course updated.", "success")
        return redirect(url_for("admin_courses"))
    return render_template("admin/admin_course_form.html", course=course, categories=categories)


@app.route("/admin/courses/<int:course_id>/delete", methods=["POST"])
@login_required
@admin_required
def admin_course_delete(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash("Course deleted.", "success")
    return redirect(url_for("admin_courses"))


# ---------- Admin: Topics ----------
@app.route("/admin/topics")
@login_required
@admin_required
def admin_topics():
    course_id = request.args.get("course_id", type=int)
    q = CourseTopic.query
    if course_id:
        q = q.filter_by(course_id=course_id)
    topics = q.order_by(CourseTopic.course_id, CourseTopic.order).all()
    courses = Course.query.order_by(Course.id).all()
    return render_template("admin/admin_topics.html", topics=topics, courses=courses, selected_course_id=course_id)


@app.route("/admin/topics/add", methods=["GET", "POST"])
@login_required
@admin_required
def admin_topic_add():
    courses = Course.query.order_by(Course.id).all()
    if request.method == "POST":
        course_id = request.form.get("course_id", type=int)
        title = request.form.get("title", "").strip()
        order = request.form.get("order", type=int) or 0
        video_url = request.form.get("video_url", "").strip()
        notes_content = request.form.get("notes_content", "").strip()
        is_test_topic = request.form.get("is_test_topic") == "1"
        
        # Handle video file upload
        video_file = request.files.get('video_file')
        final_video_url = video_url
        
        if video_file and video_file.filename:
            if not allowed_video_file(video_file.filename):
                flash("Invalid video file format. Allowed: MP4, WebM, OGG, MOV, AVI, MKV", "error")
                return render_template("admin/admin_topic_form.html", topic=None, courses=courses)
            
            # Check file size
            video_file.seek(0, os.SEEK_END)
            file_size = video_file.tell()
            video_file.seek(0)
            if file_size > MAX_VIDEO_SIZE:
                flash(f"Video file too large. Maximum size: {MAX_VIDEO_SIZE // (1024*1024)}MB", "error")
                return render_template("admin/admin_topic_form.html", topic=None, courses=courses)
            
            # Save uploaded file
            filename = secure_filename(video_file.filename)
            # Add timestamp to avoid conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name_parts = filename.rsplit('.', 1)
            filename = f"{name_parts[0]}_{timestamp}.{name_parts[1]}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            video_file.save(filepath)
            
            # Store relative URL for the video (use forward slash for web path)
            final_video_url = f"/static/uploads/videos/{filename}"
            flash(f"Video uploaded successfully: {filename}", "success")
        
        if not title or not course_id:
            flash("Title and course are required.", "error")
            return render_template("admin/admin_topic_form.html", topic=None, courses=courses)
        
        t = CourseTopic(course_id=course_id, title=title, order=order, video_url=final_video_url or None, notes_content=notes_content or None)
        if is_test_topic:
            t.course_test_questions = "[]"
        db.session.add(t)
        db.session.commit()
        flash("Topic added.", "success")
        return redirect(url_for("admin_topics", course_id=course_id))
    selected_course_id = request.args.get("course_id", type=int)
    return render_template("admin/admin_topic_form.html", topic=None, courses=courses, selected_course_id=selected_course_id)


@app.route("/admin/topics/<int:topic_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def admin_topic_edit(topic_id):
    topic = CourseTopic.query.get_or_404(topic_id)
    courses = Course.query.order_by(Course.id).all()
    if request.method == "POST":
        topic.course_id = request.form.get("course_id", type=int) or topic.course_id
        topic.title = request.form.get("title", "").strip() or topic.title
        topic.order = request.form.get("order", type=int) or 0
        video_url = request.form.get("video_url", "").strip()
        
        # Handle video file upload
        video_file = request.files.get('video_file')
        final_video_url = video_url
        
        if video_file and video_file.filename:
            if not allowed_video_file(video_file.filename):
                flash("Invalid video file format. Allowed: MP4, WebM, OGG, MOV, AVI, MKV", "error")
                return render_template("admin/admin_topic_form.html", topic=topic, courses=courses)
            
            # Check file size
            video_file.seek(0, os.SEEK_END)
            file_size = video_file.tell()
            video_file.seek(0)
            if file_size > MAX_VIDEO_SIZE:
                flash(f"Video file too large. Maximum size: {MAX_VIDEO_SIZE // (1024*1024)}MB", "error")
                return render_template("admin/admin_topic_form.html", topic=topic, courses=courses)
            
            # Delete old uploaded video if exists
            if topic.video_url and topic.video_url.startswith('/static/uploads/videos/'):
                old_filename = topic.video_url.split('/')[-1]
                old_filepath = os.path.join(UPLOAD_FOLDER, old_filename)
                if os.path.exists(old_filepath):
                    try:
                        os.remove(old_filepath)
                    except Exception:
                        pass
            
            # Save new uploaded file
            filename = secure_filename(video_file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name_parts = filename.rsplit('.', 1)
            filename = f"{name_parts[0]}_{timestamp}.{name_parts[1]}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            video_file.save(filepath)
            
            # Store relative URL for the video (use forward slash for web path)
            final_video_url = f"/static/uploads/videos/{filename}"
            flash(f"Video uploaded successfully: {filename}", "success")
        
        topic.video_url = final_video_url or None
        topic.notes_content = request.form.get("notes_content", "").strip() or None
        db.session.commit()
        flash("Topic updated.", "success")
        return redirect(url_for("admin_topics", course_id=topic.course_id))
    return render_template("admin/admin_topic_form.html", topic=topic, courses=courses)


@app.route("/admin/topics/<int:topic_id>/delete", methods=["POST"])
@login_required
@admin_required
def admin_topic_delete(topic_id):
    topic = CourseTopic.query.get_or_404(topic_id)
    cid = topic.course_id
    db.session.delete(topic)
    db.session.commit()
    flash("Topic deleted.", "success")
    return redirect(url_for("admin_topics", course_id=cid))


# ---------- Admin: Quiz questions (per topic) ----------
@app.route("/admin/quiz-questions")
@login_required
@admin_required
def admin_quiz_questions():
    topic_id = request.args.get("topic_id", type=int)
    topics = CourseTopic.query.order_by(CourseTopic.course_id, CourseTopic.order).all()
    topic = CourseTopic.query.get(topic_id) if topic_id else None
    questions = []
    if topic and topic.quiz_questions:
        try:
            questions = json.loads(topic.quiz_questions)
        except Exception:
            pass
    return render_template("admin/admin_quiz_questions.html", topic=topic, topics=topics, questions=questions)


@app.route("/admin/quiz-questions/<int:topic_id>/save", methods=["POST"])
@login_required
@admin_required
def admin_quiz_questions_save(topic_id):
    topic = CourseTopic.query.get_or_404(topic_id)
    data = request.get_json() or {}
    questions = data.get("questions", [])
    validated = []
    for q in questions:
        question = (q.get("question") or "").strip()
        options = q.get("options") or []
        if isinstance(options, str):
            options = [o.strip() for o in options.split("\n") if o.strip()]
        correct_index = int(q.get("correct_index", 0))
        if question and len(options) >= 2:
            validated.append({"question": question, "options": options, "correct_index": min(correct_index, len(options) - 1)})
    topic.quiz_questions = json.dumps(validated)
    db.session.commit()
    return jsonify({"ok": True})


# ---------- Admin: Test questions (per course - stored in test topic) ----------
@app.route("/admin/test-questions")
@login_required
@admin_required
def admin_test_questions():
    course_id = request.args.get("course_id", type=int)
    courses = Course.query.order_by(Course.id).all()
    course = Course.query.get(course_id) if course_id else None
    test_topic = None
    questions = []
    if course:
        test_topic = CourseTopic.query.filter_by(course_id=course.id).filter(CourseTopic.course_test_questions.isnot(None)).first()
        if test_topic and test_topic.course_test_questions:
            try:
                questions = json.loads(test_topic.course_test_questions)
            except Exception:
                pass
    return render_template("admin/admin_test_questions.html", course=course, courses=courses, test_topic=test_topic, questions=questions)


@app.route("/admin/test-questions/<int:course_id>/save", methods=["POST"])
@login_required
@admin_required
def admin_test_questions_save(course_id):
    course = Course.query.get_or_404(course_id)
    test_topic = CourseTopic.query.filter_by(course_id=course_id).filter(CourseTopic.course_test_questions.isnot(None)).first()
    if not test_topic:
        test_topic = CourseTopic(course_id=course_id, title="Course Test", order=999, course_test_questions="[]")
        db.session.add(test_topic)
        db.session.commit()
    data = request.get_json() or {}
    questions = data.get("questions", [])
    validated = []
    for q in questions:
        question = (q.get("question") or "").strip()
        options = q.get("options") or []
        if isinstance(options, str):
            options = [o.strip() for o in options.split("\n") if o.strip()]
        correct_index = int(q.get("correct_index", 0))
        if question and len(options) >= 2:
            validated.append({"question": question, "options": options, "correct_index": min(correct_index, len(options) - 1)})
    test_topic.course_test_questions = json.dumps(validated)
    db.session.commit()
    return jsonify({"ok": True})


def _upgrade_schema():
    """Add missing columns to existing tables (e.g. after model changes)."""
    with app.app_context():
        try:
            if "sqlite" in db.engine.url.drivername:
                r = db.session.execute(db.text("PRAGMA table_info(users)")).fetchall()
                cols = [row[1] for row in r]
                if "student_id" not in cols:
                    db.session.execute(db.text("ALTER TABLE users ADD COLUMN student_id VARCHAR(20)"))
                    db.session.commit()
        except Exception:
            db.session.rollback()


def init_db():
    os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)
    with app.app_context():
        db.create_all()
        _upgrade_schema()


if __name__ == "__main__":
    init_db()
    print("TECH Skills Development - Starting server at http://127.0.0.1:5000")
    print("Run 'python seed_data.py' once to add categories and courses.")
    print("Press CTRL+C to stop the server.")
    app.run(host="127.0.0.1", debug=True, port=5000, use_reloader=True)
