"""Update existing categories and courses with new names and durations."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, Category, Course

# New category data
CATEGORIES_DATA = {
    "basic-computer": {
        "name": "Basic Computer Courses",
        "description": "Computer fundamentals, MS Office, internet & email, hardware, networking and digital literacy.",
        "icon": "💻"
    },
    "coding-languages": {
        "name": "Programming Language Courses",
        "description": "C, C++, Java, Python, JavaScript, PHP, C#, Ruby, Kotlin and Swift.",
        "icon": "⌨️"
    },
    "finance": {
        "name": "Finance & Accounting",
        "description": "Basics of finance, accounting, personal finance, banking, investment and taxation.",
        "icon": "📊"
    },
    "digital-marketing": {
        "name": "Digital Marketing",
        "description": "Digital marketing fundamentals, SEO, SMM, content, email, PPC and analytics.",
        "icon": "📱"
    },
    "data-science": {
        "name": "Data Science / AI / ML",
        "description": "Data science with Python, ML, AI, deep learning, statistics, SQL and NLP.",
        "icon": "📈"
    },
    "trading": {
        "name": "Trading & Stock Market",
        "description": "Stock market basics, intraday, options, futures, commodities, forex and trading risk management.",
        "icon": "📉"
    }
}

# New course names by category
COURSES_BY_CATEGORY = {
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

# Durations in hours (varied)
BASE_DURATIONS_HOURS = [10, 12, 14, 5, 8, 9, 6, 7, 11, 15]


def update_categories_and_courses():
    """Update existing categories and courses with new names and durations."""
    with app.app_context():
        print("Starting update of categories and courses...")
        
        # Update categories (remove descriptions)
        for slug, data in CATEGORIES_DATA.items():
            cat = Category.query.filter_by(slug=slug).first()
            if cat:
                old_name = cat.name
                cat.name = data["name"]
                cat.description = ""  # Remove description
                cat.icon = data["icon"]
                print(f"Updated category: {old_name} -> {data['name']} (description removed)")
            else:
                # Create if doesn't exist
                cat = Category(
                    name=data["name"],
                    slug=slug,
                    description="",  # No description
                    icon=data["icon"]
                )
                db.session.add(cat)
                print(f"Created category: {data['name']}")
        
        db.session.commit()
        print("Categories updated.")
        
        # Update courses
        categories = {cat.slug: cat for cat in Category.query.all()}
        
        for cat_slug, course_names in COURSES_BY_CATEGORY.items():
            cat = categories.get(cat_slug)
            if not cat:
                print(f"Warning: Category '{cat_slug}' not found, skipping courses.")
                continue
            
            # Get existing courses for this category
            existing_courses = Course.query.filter_by(category_id=cat.id).order_by(Course.id).all()
            
            # Update existing courses or create new ones
            for i, new_name in enumerate(course_names, start=1):
                course_slug = f"{cat_slug}-course-{i}"
                duration_hours = BASE_DURATIONS_HOURS[(i - 1) % len(BASE_DURATIONS_HOURS)]
                
                # Try to find existing course by slug or by position
                course = Course.query.filter_by(slug=course_slug).first()
                
                if not course and i <= len(existing_courses):
                    # Update existing course at this position
                    course = existing_courses[i - 1]
                    course.slug = course_slug
                
                if course:
                    old_name = course.name
                    course.name = new_name
                    course.duration_weeks = duration_hours  # Store hours in duration_weeks column
                    course.description = f"Learn {new_name} with video lessons, notes, quizzes and a final test."
                    course.syllabus_text = (
                        "Module 1: Introduction and setup.\n"
                        "Module 2: Core concepts and hands-on exercises.\n"
                        "Module 3: Advanced practice and mini projects.\n"
                        "Module 4: Final assessment and next steps."
                    )
                    print(f"  Updated course: {old_name} -> {new_name} ({duration_hours} hours)")
                else:
                    # Create new course
                    course = Course(
                        category_id=cat.id,
                        name=new_name,
                        slug=course_slug,
                        description=f"Learn {new_name} with video lessons, notes, quizzes and a final test.",
                        duration_weeks=duration_hours,
                        syllabus_text=(
                            "Module 1: Introduction and setup.\n"
                            "Module 2: Core concepts and hands-on exercises.\n"
                            "Module 3: Advanced practice and mini projects.\n"
                            "Module 4: Final assessment and next steps."
                        )
                    )
                    db.session.add(course)
                    print(f"  Created course: {new_name} ({duration_hours} hours)")
        
        db.session.commit()
        print("\nUpdate completed! Categories and courses have been renamed and durations updated to hours.")
        print("Note: Course durations are stored in the 'duration_weeks' column but represent hours.")


if __name__ == "__main__":
    update_categories_and_courses()
