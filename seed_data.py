"""Seed database with categories, courses, topics, and sample quiz/test questions."""
import os
import sys
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, Category, Course, CourseTopic

# Sample topic quiz (5 questions per topic)
SAMPLE_QUIZ = [
    {"question": "What is the main purpose of this topic?", "options": ["To introduce concepts", "To conclude", "To test", "To skip"], "correct_index": 0},
    {"question": "Which option best describes the content?", "options": ["Theoretical", "Practical", "Both", "None"], "correct_index": 2},
    {"question": "How many sections does this topic cover?", "options": ["One", "Two", "Three", "Four"], "correct_index": 2},
    {"question": "What should you do after watching the video?", "options": ["Skip notes", "Read notes and take quiz", "Only quiz", "Nothing"], "correct_index": 1},
    {"question": "Completing the quiz unlocks the next topic.", "options": ["True", "False"], "correct_index": 0},
]

# Course test (20 questions)
SAMPLE_COURSE_TEST = [
    {"question": "What is the first step in learning this subject?", "options": ["Introduction", "Conclusion", "Test", "Skip"], "correct_index": 0},
    {"question": "Which is not a component of the course?", "options": ["Video", "Notes", "Quiz", "Games"], "correct_index": 3},
    {"question": "How many topics are typically in a module?", "options": ["1", "3", "5", "10"], "correct_index": 2},
    {"question": "What does MCQ stand for?", "options": ["Multiple Choice Question", "Many Correct Queries", "Multiple Check Question", "None"], "correct_index": 0},
    {"question": "Passing the quiz requires at least:", "options": ["40%", "50%", "60%", "100%"], "correct_index": 2},
    {"question": "The course test has how many questions?", "options": ["5", "10", "15", "20"], "correct_index": 3},
    {"question": "Correct answers are shown in:", "options": ["Red", "Green", "Blue", "Yellow"], "correct_index": 1},
    {"question": "Incorrect answers are shown in:", "options": ["Green", "Red", "Blue", "Yellow"], "correct_index": 1},
    {"question": "You can go back to previous questions using:", "options": ["Next", "Previous", "Finish", "Skip"], "correct_index": 1},
    {"question": "On the last question, you click:", "options": ["Next", "Previous", "Finish", "Cancel"], "correct_index": 2},
    {"question": "Enrollment is confirmed via:", "options": ["Automatic", "Popup with Yes/Cancel", "Email only", "None"], "correct_index": 1},
    {"question": "After enrolling you see:", "options": ["Payment", "Topic list", "Certificate", "Nothing"], "correct_index": 1},
    {"question": "The first topic is always:", "options": ["Locked", "Unlocked", "Hidden", "Optional"], "correct_index": 1},
    {"question": "Notes contain:", "options": ["Only links", "Key points and summaries", "Videos", "Nothing"], "correct_index": 1},
    {"question": "TECH Skills Development offers courses in:", "options": ["One category", "Few categories", "Multiple categories", "None"], "correct_index": 2},
    {"question": "Admin login is separate from student login.", "options": ["True", "False"], "correct_index": 0},
    {"question": "You can change your password in:", "options": ["Home", "Settings", "Course", "Nowhere"], "correct_index": 1},
    {"question": "Profile details include:", "options": ["Phone, DOB, Address", "Only email", "Only name", "Nothing"], "correct_index": 0},
    {"question": "Categories on home include:", "options": ["Basic computer", "Coding languages", "Finance", "All of these"], "correct_index": 3},
    {"question": "Completing a topic quiz with 60% or more:", "options": ["Locks next topic", "Unlocks next topic", "Does nothing", "Resets progress"], "correct_index": 1},
]

# Notes content for topics
NOTES_INTRO = """Introduction — Key Points

This topic introduces you to the course structure and learning objectives.

What you will learn:
• How the course is organized
• How to navigate video, notes, and quiz
• How unlocking works (complete one topic to unlock the next)

Take your time with the video and notes, then attempt the quiz. Good luck!
"""

NOTES_TOPIC2 = """Core Concepts — Summary

This section covers the main concepts of the module.

Key takeaways:
• Concept A: Definition and use cases
• Concept B: How it relates to the first topic
• Concept C: Practical applications

Review the video if needed, then complete the quiz to unlock the next topic.
"""

NOTES_TOPIC3 = """Advanced Ideas — Notes

Here we build on the previous topics.

Summary:
• Advanced idea 1
• Advanced idea 2
• How they connect to the full course

After the quiz you will be able to attempt the full course test.
"""


def seed():
    with app.app_context():
        # Create tables if they don't exist
        from app import init_db
        init_db()
        if Category.query.first():
            print("Data already exists. Skipping seed.")
            return
        # Categories - aligned with requested topics
        categories_data = [
            (
                "Basic Computer Courses",
                "basic-computer",
                "Computer fundamentals, MS Office, internet & email, hardware, networking and digital literacy.",
                "💻",
            ),
            (
                "Programming Language Courses",
                "coding-languages",
                "C, C++, Java, Python, JavaScript, PHP, C#, Ruby, Kotlin and Swift.",
                "⌨️",
            ),
            (
                "Finance & Accounting",
                "finance",
                "Basics of finance, accounting, personal finance, banking, investment and taxation.",
                "📊",
            ),
            (
                "Digital Marketing",
                "digital-marketing",
                "Digital marketing fundamentals, SEO, SMM, content, email, PPC and analytics.",
                "📱",
            ),
            (
                "Data Science / AI / ML",
                "data-science",
                "Data science with Python, ML, AI, deep learning, statistics, SQL and NLP.",
                "📈",
            ),
            (
                "Trading & Stock Market",
                "trading",
                "Stock market basics, intraday, options, futures, commodities, forex and trading risk management.",
                "📉",
            ),
        ]
        for name, slug, desc, icon in categories_data:
            c = Category(name=name, slug=slug, description=desc, icon=icon)
            db.session.add(c)
        db.session.commit()

        categories = {cat.slug: cat for cat in Category.query.all()}

        # Courses per category - mapped to detailed topic lists
        courses_by_category = {
            "basic-computer": [
                "Computer Fundamentals",
                "MS Office (Word, Excel, PowerPoint)",
                "Internet & Email Basics",
                "Windows Operating System Basics",
                "Typing Skills (English)",
                "Computer Hardware & Maintenance",
                "Basic Networking Concepts",
                "Cyber Safety & Security Basics",
                "Introduction to Cloud Computing",
                "Digital Literacy Course",
            ],
            "coding-languages": [
                "C Programming",
                "C++ Programming",
                "Java Programming",
                "Python Programming",
                "JavaScript",
                "PHP",
                "C# (.NET)",
                "Ruby Programming",
                "Kotlin Programming",
                "Swift Programming",
            ],
            "finance": [
                "Basics of Finance",
                "Financial Accounting",
                "Corporate Finance",
                "Personal Finance Management",
                "Banking & Financial Services",
                "Investment Management",
                "Taxation Basics",
                "Financial Planning",
                "Risk Management",
                "Budgeting & Financial Analysis",
            ],
            "digital-marketing": [
                "Digital Marketing Fundamentals",
                "Search Engine Optimization (SEO)",
                "Social Media Marketing (SMM)",
                "Content Marketing",
                "Email Marketing",
                "Google Ads & PPC",
                "Affiliate Marketing",
                "Mobile Marketing",
                "Web Analytics",
                "Online Branding & Strategy",
            ],
            "data-science": [
                "Data Science with Python",
                "Data Analysis with Python",
                "Machine Learning",
                "Artificial Intelligence (AI)",
                "Deep Learning",
                "Data Visualization",
                "Statistics for Data Science",
                "Big Data Analytics",
                "SQL for Data Science",
                "Natural Language Processing (NLP)",
            ],
            "trading": [
                "Stock Market Basics",
                "Equity Trading",
                "Intraday Trading",
                "Technical Analysis",
                "Fundamental Analysis",
                "Options Trading",
                "Futures Trading",
                "Commodity Trading",
                "Forex Trading",
                "Risk Management in Trading",
            ],
        }

        # Durations in HOURS (varied) – reused across categories
        base_durations_hours = [10, 12, 14, 5, 8, 9, 6, 7, 11, 15]

        def add_courses(cat_slug, course_names):
            cat = categories[cat_slug]
            for i, name in enumerate(course_names, start=1):
                slug = cat_slug + "-course-" + str(i)
                duration_hours = base_durations_hours[(i - 1) % len(base_durations_hours)]
                course = Course(
                    category_id=cat.id,
                    name=name,
                    slug=slug,
                    description="Learn " + name + " with video lessons, notes, quizzes and a final test.",
                    # Store duration in hours (column name kept for compatibility)
                    duration_weeks=duration_hours,
                    syllabus_text=(
                        "Module 1: Introduction and setup.\n"
                        "Module 2: Core concepts and hands-on exercises.\n"
                        "Module 3: Advanced practice and mini projects.\n"
                        "Module 4: Final assessment and next steps."
                    ),
                )
                db.session.add(course)
        for slug, names in courses_by_category.items():
            add_courses(slug, names)
        db.session.commit()

        topics_data = [
            (1, "Introduction", None, NOTES_INTRO, SAMPLE_QUIZ, None),
            (2, "Core Concepts", None, NOTES_TOPIC2, SAMPLE_QUIZ, None),
            (3, "Advanced Ideas", None, NOTES_TOPIC3, SAMPLE_QUIZ, None),
            (4, "Course Test (20 questions)", None, None, None, SAMPLE_COURSE_TEST),
            (5, "Certificate", None, "Complete the course test to unlock your certificate.", None, None),  # 5th topic - certificate only
        ]
        first_course = Course.query.filter_by(slug="basic-computer-course-1").first()
        if first_course:
            for order, title, video_url, notes, quiz_q, test_q in topics_data:
                t = CourseTopic(
                    course_id=first_course.id,
                    title=title,
                    order=order,
                    video_url=video_url or "",
                    notes_content=notes or "",
                    quiz_questions=json.dumps(quiz_q) if quiz_q else None,
                    course_test_questions=json.dumps(test_q) if test_q else None,
                )
                db.session.add(t)

        # Add same structure to a few more courses so every category has at least one full course
        for slug in ["coding-languages-course-1", "finance-course-1"]:
            co = Course.query.filter_by(slug=slug).first()
            if co:
                for order, title, video_url, notes, quiz_q, test_q in topics_data:
                    t = CourseTopic(
                        course_id=co.id,
                        title=title,
                        order=order,
                        video_url=video_url or "",
                        notes_content=notes or "",
                        quiz_questions=json.dumps(quiz_q) if quiz_q else None,
                        course_test_questions=json.dumps(test_q) if test_q else None,
                    )
                    db.session.add(t)

        db.session.commit()
        print("Seed completed. Categories, courses, and topics added.")


if __name__ == "__main__":
    seed()
