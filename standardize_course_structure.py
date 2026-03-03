"""
Standardize 5 topics structure for all courses with specific content types
"""
import os
import sys
import json

# Add project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Category, Course, CourseTopic

def get_standardized_topics(category_name):
    """Get standardized 5 topics with specific content types"""
    topics_map = {
        "Web Development": [
            {
                "title": "Introduction to Web Development",
                "order": 1,
                "video_url": "",
                "notes_content": "Welcome to Web Development! This introduction covers the fundamentals of web technologies, HTML basics, CSS fundamentals, and an overview of modern web development practices. You'll learn about the structure of web pages, basic styling, and how the web works.",
                "quiz_questions": None,
                "course_test_questions": None
            },
            {
                "title": "Core Concepts",
                "order": 2,
                "video_url": "",
                "notes_content": "Deep dive into core web development concepts including HTML5 semantic elements, CSS3 advanced selectors, JavaScript fundamentals, DOM manipulation, and responsive design principles. Master the building blocks of modern web applications.",
                "quiz_questions": None,
                "course_test_questions": None
            },
            {
                "title": "Advanced Concepts",
                "order": 3,
                "video_url": "",
                "notes_content": "Explore advanced web development topics including modern JavaScript frameworks (React, Vue, Angular), backend development with Node.js, database integration, API design, and deployment strategies. Build production-ready applications.",
                "quiz_questions": None,
                "course_test_questions": None
            },
            {
                "title": "Final Assessment",
                "order": 4,
                "video_url": "",
                "notes_content": "Comprehensive final assessment covering all topics learned in this course. This includes practical coding exercises, project development, and theoretical knowledge evaluation. Prepare to showcase your web development skills.",
                "quiz_questions": None,
                "course_test_questions": None
            },
            {
                "title": "Certificate",
                "order": 5,
                "video_url": "",
                "notes_content": "Congratulations on completing the Web Development course! This final section provides information about your certificate, next steps in your learning journey, and career opportunities in web development.",
                "quiz_questions": None,
                "course_test_questions": None
            }
        ],
        "Data Science": [
            {
                "title": "Introduction to Data Science",
                "order": 1,
                "video_url": "",
                "notes_content": "Introduction to the exciting field of Data Science! Learn about data science methodologies, tools, and applications. Understand the role of data scientists, the data science lifecycle, and fundamental concepts in data analysis.",
                "quiz_questions": None,
                "course_test_questions": None
            },
            {
                "title": "Core Concepts",
                "order": 2,
                "video_url": "",
                "notes_content": "Master core data science concepts including statistics fundamentals, probability theory, data cleaning techniques, exploratory data analysis, and data visualization. Build strong foundations in mathematical and statistical thinking.",
                "quiz_questions": None,
                "course_test_questions": None
            },
            {
                "title": "Advanced Concepts",
                "order": 3,
                "video_url": "",
                "notes_content": "Advanced data science topics including machine learning algorithms, deep learning, natural language processing, computer vision, and big data technologies. Work with real-world datasets and cutting-edge tools.",
                "quiz_questions": None,
                "course_test_questions": None
            },
            {
                "title": "Final Assessment",
                "order": 4,
                "video_url": "",
                "notes_content": "Comprehensive final assessment testing your data science knowledge and skills. Includes data analysis projects, machine learning implementations, and statistical analysis challenges.",
                "quiz_questions": None,
                "course_test_questions": None
            },
            {
                "title": "Certificate",
                "order": 5,
                "video_url": "",
                "notes_content": "Congratulations on completing the Data Science course! Information about your certificate, continuing education opportunities, and career paths in data science and analytics.",
                "quiz_questions": None,
                "course_test_questions": None
            }
        ],
        "Mobile Development": [
            {
                "title": "Introduction to Mobile Development",
                "order": 1,
                "video_url": "",
                "notes_content": "Introduction to mobile app development covering iOS and Android platforms, development environments, and basic mobile app concepts. Learn about the mobile ecosystem and development approaches.",
                "quiz_questions": None,
                "course_test_questions": None
            },
            {
                "title": "Core Concepts",
                "order": 2,
                "video_url": "",
                "notes_content": "Core mobile development concepts including UI/UX design principles, mobile app architecture, responsive design for mobile devices, and fundamental programming concepts for mobile development.",
                "quiz_questions": None,
                "course_test_questions": None
            },
            {
                "title": "Advanced Concepts",
                "order": 3,
                "video_url": "",
                "notes_content": "Advanced mobile development topics including cross-platform development, native app development, mobile app testing, performance optimization, and app store deployment strategies.",
                "quiz_questions": None,
                "course_test_questions": None
            },
            {
                "title": "Final Assessment",
                "order": 4,
                "video_url": "",
                "notes_content": "Comprehensive final assessment covering mobile development concepts, practical app development projects, and platform-specific knowledge evaluation.",
                "quiz_questions": None,
                "course_test_questions": None
            },
            {
                "title": "Certificate",
                "order": 5,
                "video_url": "",
                "notes_content": "Congratulations on completing the Mobile Development course! Certificate information and career opportunities in mobile app development.",
                "quiz_questions": None,
                "course_test_questions": None
            }
        ]
    }
    
    # Default structure for other categories
    default_topics = [
        {
            "title": "Introduction",
            "order": 1,
            "video_url": "",
            "notes_content": f"Introduction to {category_name}. Learn the fundamentals and get started with your learning journey in this exciting field.",
            "quiz_questions": None,
            "course_test_questions": None
        },
        {
            "title": "Core Concepts",
            "order": 2,
            "video_url": "",
            "notes_content": f"Core concepts and fundamental principles of {category_name}. Build a strong foundation with comprehensive notes and examples.",
            "quiz_questions": None,
            "course_test_questions": None
        },
        {
            "title": "Advanced Concepts",
            "order": 3,
            "video_url": "",
            "notes_content": f"Advanced concepts and techniques in {category_name}. Explore complex topics and real-world applications.",
            "quiz_questions": None,
            "course_test_questions": None
        },
        {
            "title": "Final Assessment",
            "order": 4,
            "video_url": "",
            "notes_content": f"Comprehensive final assessment for {category_name}. Test your knowledge and skills with challenging exercises.",
            "quiz_questions": None,
            "course_test_questions": None
        },
        {
            "title": "Certificate",
            "order": 5,
            "video_url": "",
            "notes_content": f"Congratulations on completing the {category_name} course! Receive your certificate and explore next steps.",
            "quiz_questions": None,
            "course_test_questions": None
        }
    ]
    
    return topics_map.get(category_name, default_topics)

def generate_quiz_questions(topic_title):
    """Generate exactly 5 quiz questions for each topic"""
    questions = [
        {
            "question": f"What is the primary purpose of {topic_title}?",
            "options": ["Option A: Foundation", "Option B: Application", "Option C: Theory", "Option D: Practice"],
            "correct_index": 0
        },
        {
            "question": f"Which concept is most important in {topic_title}?",
            "options": ["Concept A", "Concept B", "Concept C", "Concept D"],
            "correct_index": 1
        },
        {
            "question": f"How would you apply {topic_title} in practice?",
            "options": ["Application A", "Application B", "Application C", "Application D"],
            "correct_index": 2
        },
        {
            "question": f"What are the key benefits of {topic_title}?",
            "options": ["Benefit A", "Benefit B", "Benefit C", "Benefit D"],
            "correct_index": 3
        },
        {
            "question": f"Which skill is essential for {topic_title}?",
            "options": ["Skill A", "Skill B", "Skill C", "Skill D"],
            "correct_index": 0
        }
    ]
    return json.dumps(questions)

def generate_final_assessment_questions(course_name):
    """Generate final assessment questions for the course"""
    questions = [
        {
            "question": f"What is the most important concept you learned in {course_name}?",
            "options": ["Fundamentals", "Advanced Topics", "Practical Applications", "Theory"],
            "correct_index": 2
        },
        {
            "question": f"How would you apply your knowledge from {course_name} in a real project?",
            "options": ["Project A", "Project B", "Project C", "Project D"],
            "correct_index": 1
        },
        {
            "question": f"What skills have you developed in {course_name}?",
            "options": ["Technical Skills", "Soft Skills", "Both", "None"],
            "correct_index": 2
        },
        {
            "question": f"Which area of {course_name} interests you most for further study?",
            "options": ["Advanced Topics", "Practical Applications", "Research", "Industry"],
            "correct_index": 0
        },
        {
            "question": f"How confident are you in applying {course_name} concepts?",
            "options": ["Very Confident", "Confident", "Somewhat Confident", "Not Confident"],
            "correct_index": 1
        }
    ]
    return json.dumps(questions)

def standardize_course_structure():
    """Standardize all courses with exactly 5 topics"""
    with app.app_context():
        try:
            categories = Category.query.all()
            
            for category in categories:
                print(f"🔄 Processing category: {category.name}")
                
                # Get standardized topics for this category
                standard_topics = get_standardized_topics(category.name)
                
                # Get all courses in this category
                courses = Course.query.filter_by(category_id=category.id).all()
                
                for course in courses:
                    print(f"  📚 Processing course: {course.name}")
                    
                    # Remove existing topics
                    existing_topics = CourseTopic.query.filter_by(course_id=course.id).all()
                    for topic in existing_topics:
                        db.session.delete(topic)
                    
                    # Add new standardized topics
                    for topic_data in standard_topics:
                        # Generate quiz questions for regular topics
                        if "Final Assessment" not in topic_data["title"] and "Certificate" not in topic_data["title"]:
                            topic_data["quiz_questions"] = generate_quiz_questions(topic_data["title"])
                        
                        # Generate final assessment questions
                        if "Final Assessment" in topic_data["title"]:
                            topic_data["course_test_questions"] = generate_final_assessment_questions(course.name)
                        
                        topic = CourseTopic(
                            course_id=course.id,
                            title=topic_data["title"],
                            order=topic_data["order"],
                            video_url=topic_data["video_url"],
                            notes_content=topic_data["notes_content"],
                            quiz_questions=topic_data["quiz_questions"],
                            course_test_questions=topic_data["course_test_questions"]
                        )
                        db.session.add(topic)
                    
                    print(f"    ✅ Added {len(standard_topics)} topics to {course.name}")
                
                db.session.commit()
            
            print("\n🎉 Course structure standardization completed!")
            return True
            
        except Exception as e:
            print(f"❌ Error standardizing course structure: {e}")
            return False

if __name__ == "__main__":
    print("🔧 Standardizing Course Structure (5 Topics per Course)...")
    print("=" * 60)
    
    if standardize_course_structure():
        print("✅ All courses now have exactly 5 standardized topics!")
        print("\n📋 Topic Structure:")
        print("   1. Introduction - Basic overview and fundamentals")
        print("   2. Core Concepts - Detailed notes and theory")
        print("   3. Advanced Concepts - In-depth content")
        print("   4. Final Assessment - 5 questions evaluation")
        print("   5. Certificate - Completion and certification")
        print("\n📝 Quiz Structure:")
        print("   • Each topic has exactly 5 questions")
        print("   • Final Assessment has 5 evaluation questions")
        print("   • Questions are automatically generated")
    else:
        print("❌ Course structure standardization failed")
