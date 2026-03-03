"""
Standardize 5 topics for all courses in each category
"""
import os
import sys
import json

# Add project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Category, Course, CourseTopic

def get_standard_topics(category_name):
    """Get standard 5 topics based on category"""
    topics_map = {
        "Web Development": [
            {"title": "HTML & CSS Fundamentals", "order": 1, "video_url": "", "notes_content": "Learn the basics of HTML and CSS"},
            {"title": "JavaScript Essentials", "order": 2, "video_url": "", "notes_content": "Master JavaScript programming fundamentals"},
            {"title": "React.js Basics", "order": 3, "video_url": "", "notes_content": "Introduction to React.js framework"},
            {"title": "Backend Development", "order": 4, "video_url": "", "notes_content": "Server-side programming with Node.js"},
            {"title": "Full Stack Project", "order": 5, "video_url": "", "notes_content": "Build a complete full-stack application"}
        ],
        "Data Science": [
            {"title": "Python for Data Science", "order": 1, "video_url": "", "notes_content": "Python programming for data analysis"},
            {"title": "Data Analysis with Pandas", "order": 2, "video_url": "", "notes_content": "Data manipulation and analysis with Pandas"},
            {"title": "Machine Learning Basics", "order": 3, "video_url": "", "notes_content": "Introduction to machine learning concepts"},
            {"title": "Data Visualization", "order": 4, "video_url": "", "notes_content": "Creating visualizations with Matplotlib and Seaborn"},
            {"title": "Deep Learning Fundamentals", "order": 5, "video_url": "", "notes_content": "Neural networks and deep learning basics"}
        ],
        "Mobile Development": [
            {"title": "Mobile UI/UX Design", "order": 1, "video_url": "", "notes_content": "Design principles for mobile applications"},
            {"title": "React Native Basics", "order": 2, "video_url": "", "notes_content": "Building mobile apps with React Native"},
            {"title": "Flutter Fundamentals", "order": 3, "video_url": "", "notes_content": "Cross-platform development with Flutter"},
            {"title": "Mobile App Testing", "order": 4, "video_url": "", "notes_content": "Testing strategies for mobile applications"},
            {"title": "App Deployment", "order": 5, "video_url": "", "notes_content": "Publishing apps to app stores"}
        ],
        "Cloud Computing": [
            {"title": "Cloud Fundamentals", "order": 1, "video_url": "", "notes_content": "Introduction to cloud computing concepts"},
            {"title": "AWS Services", "order": 2, "video_url": "", "notes_content": "Amazon Web Services overview"},
            {"title": "Azure Platform", "order": 3, "video_url": "", "notes_content": "Microsoft Azure cloud services"},
            {"title": "Google Cloud Platform", "order": 4, "video_url": "", "notes_content": "Google Cloud services and tools"},
            {"title": "Cloud Architecture", "order": 5, "video_url": "", "notes_content": "Designing scalable cloud architectures"}
        ],
        "Cybersecurity": [
            {"title": "Security Fundamentals", "order": 1, "video_url": "", "notes_content": "Basic cybersecurity concepts and principles"},
            {"title": "Network Security", "order": 2, "video_url": "", "notes_content": "Protecting networks from threats"},
            {"title": "Ethical Hacking", "order": 3, "video_url": "", "notes_content": "Ethical hacking and penetration testing"},
            {"title": "Cryptography", "order": 4, "video_url": "", "notes_content": "Encryption and data protection techniques"},
            {"title": "Security Compliance", "order": 5, "video_url": "", "notes_content": "Security standards and compliance frameworks"}
        ]
    }
    
    # Return default topics if category not found
    return topics_map.get(category_name, [
        {"title": "Introduction to " + category_name, "order": 1, "video_url": "", "notes_content": "Getting started with " + category_name},
        {"title": "Core Concepts", "order": 2, "video_url": "", "notes_content": "Understanding fundamental concepts"},
        {"title": "Practical Applications", "order": 3, "video_url": "", "notes_content": "Hands-on practical exercises"},
        {"title": "Advanced Techniques", "order": 4, "video_url": "", "notes_content": "Advanced methods and best practices"},
        {"title": "Project Work", "order": 5, "video_url": "", "notes_content": "Complete a real-world project"}
    ])

def generate_quiz_questions(topic_title):
    """Generate quiz questions for a topic"""
    base_questions = [
        {
            "question": f"What is the main purpose of {topic_title}?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_index": 0
        },
        {
            "question": f"Which of the following is a key concept in {topic_title}?",
            "options": ["Concept A", "Concept B", "Concept C", "Concept D"],
            "correct_index": 1
        },
        {
            "question": f"How would you apply {topic_title} in a real scenario?",
            "options": ["Application A", "Application B", "Application C", "Application D"],
            "correct_index": 2
        }
    ]
    return json.dumps(base_questions)

def standardize_course_topics():
    """Standardize topics for all courses"""
    with app.app_context():
        try:
            categories = Category.query.all()
            
            for category in categories:
                print(f"🔄 Processing category: {category.name}")
                
                # Get standard topics for this category
                standard_topics = get_standard_topics(category.name)
                
                # Get all courses in this category
                courses = Course.query.filter_by(category_id=category.id).all()
                
                for course in courses:
                    print(f"  📚 Processing course: {course.name}")
                    
                    # Remove existing topics
                    existing_topics = CourseTopic.query.filter_by(course_id=course.id).all()
                    for topic in existing_topics:
                        db.session.delete(topic)
                    
                    # Add new standard topics
                    for topic_data in standard_topics:
                        topic = CourseTopic(
                            course_id=course.id,
                            title=topic_data["title"],
                            order=topic_data["order"],
                            video_url=topic_data["video_url"],
                            notes_content=topic_data["notes_content"],
                            quiz_questions=generate_quiz_questions(topic_data["title"])
                        )
                        db.session.add(topic)
                    
                    print(f"    ✅ Added {len(standard_topics)} topics to {course.name}")
                
                db.session.commit()
            
            print("\n🎉 Course topics standardization completed!")
            return True
            
        except Exception as e:
            print(f"❌ Error standardizing topics: {e}")
            return False

if __name__ == "__main__":
    print("🔧 Standardizing Course Topics...")
    print("=" * 50)
    
    if standardize_course_topics():
        print("✅ All courses now have 5 standardized topics!")
        print("\n📋 Summary:")
        print("   • Each course has exactly 5 topics")
        print("   • Topics are category-specific")
        print("   • Each topic has quiz questions")
        print("   • Topics follow a logical progression")
    else:
        print("❌ Topic standardization failed")
