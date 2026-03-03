from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(120), nullable=True)
    role = db.Column(db.String(20), default="student")  # student | admin
    student_id = db.Column(db.String(20), unique=True, nullable=True)  # Unique identification code
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class StudentDetail(db.Model):
    __tablename__ = "student_details"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = db.relationship("User", backref=db.backref("student_detail", uselist=False))


class Complaint(db.Model):
    __tablename__ = "complaints"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)  # Can be anonymous
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", backref=db.backref("complaints", lazy="dynamic"))


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(50), nullable=True)
    courses = db.relationship("Course", backref="category", lazy="dynamic")


class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    duration_weeks = db.Column(db.Integer, default=4)
    syllabus_text = db.Column(db.Text, nullable=True)
    topics = db.relationship("CourseTopic", backref="course", lazy="dynamic", order_by="CourseTopic.order")
    enrollments = db.relationship("Enrollment", backref="course", lazy="dynamic")


class CourseTopic(db.Model):
    __tablename__ = "course_topics"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    order = db.Column(db.Integer, default=0)
    video_url = db.Column(db.String(500), nullable=True)
    notes_content = db.Column(db.Text, nullable=True)
    quiz_questions = db.Column(db.Text, nullable=True)  # JSON list of {question, options, correct_index}
    course_test_questions = db.Column(db.Text, nullable=True)  # Only for topic that is "Course Test"


class Enrollment(db.Model):
    __tablename__ = "enrollments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", backref=db.backref("enrollments", lazy="dynamic"))


class TopicProgress(db.Model):
    __tablename__ = "topic_progress"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey("course_topics.id"), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", backref=db.backref("topic_progress", lazy="dynamic"))


class TopicQuizAttempt(db.Model):
    __tablename__ = "topic_quiz_attempts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey("course_topics.id"), nullable=False)
    score_percent = db.Column(db.Float, nullable=False)
    answers_json = db.Column(db.Text, nullable=True)  # list of {question_index, selected_index, correct}
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)


class CourseTestAttempt(db.Model):
    __tablename__ = "course_test_attempts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    score_percent = db.Column(db.Float, nullable=False)
    answers_json = db.Column(db.Text, nullable=True)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)
