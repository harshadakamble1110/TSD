"""
Database initialization and error fixes for TECH Skills Development
"""
import os
import sys
from datetime import datetime
from sqlalchemy import text

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, StudentDetail, Category, Course, CourseTopic, Enrollment, TopicProgress, TopicQuizAttempt, CourseTestAttempt, Complaint

def init_database():
    """Initialize database with proper error handling"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Check if admin user exists
            admin_user = User.query.filter_by(username="Admin10").first()
            if not admin_user:
                admin_user = User(
                    username="Admin10",
                    email="admin@techskills.com",
                    full_name="System Administrator",
                    role="admin"
                )
                admin_user.set_password("1234567890")
                db.session.add(admin_user)
                db.session.commit()
                print("✅ Admin user created successfully!")
            else:
                print("✅ Admin user already exists!")
            
            return True
            
        except Exception as e:
            print(f"❌ Database initialization error: {e}")
            return False

def check_data_integrity():
    """Check and fix data integrity issues"""
    with app.app_context():
        try:
            # Check for orphaned records
            orphaned_enrollments = db.session.execute(
                text("""SELECT e.id FROM enrollments e 
                   LEFT JOIN users u ON e.user_id = u.id 
                   WHERE u.id IS NULL""")
            ).fetchall()
            
            if orphaned_enrollments:
                print(f"⚠️  Found {len(orphaned_enrollments)} orphaned enrollments")
                # Clean up orphaned records
                for enrollment_id in orphaned_enrollments:
                    db.session.execute(text("DELETE FROM enrollments WHERE id = :id"), {"id": enrollment_id[0]})
                db.session.commit()
                print("✅ Cleaned up orphaned enrollments")
            
            # Check for missing foreign keys
            missing_categories = db.session.execute(
                text("""SELECT c.id FROM courses c 
                   LEFT JOIN categories cat ON c.category_id = cat.id 
                   WHERE cat.id IS NULL""")
            ).fetchall()
            
            if missing_categories:
                print(f"⚠️  Found {len(missing_categories)} courses with missing categories")
                # Create default category
                default_category = Category.query.filter_by(slug="general").first()
                if not default_category:
                    default_category = Category(
                        name="General",
                        slug="general",
                        description="General category for uncategorized courses",
                        icon="fa-folder"
                    )
                    db.session.add(default_category)
                    db.session.commit()
                    print("✅ Created default category")
                
                # Update orphaned courses
                for course_id in missing_categories:
                    db.session.execute(
                        text("UPDATE courses SET category_id = :cat_id WHERE id = :course_id"),
                        {"cat_id": default_category.id, "course_id": course_id[0]}
                    )
                db.session.commit()
                print("✅ Updated orphaned courses")
            
            return True
            
        except Exception as e:
            print(f"❌ Data integrity check error: {e}")
            return False

def fix_template_issues():
    """Fix common template issues"""
    fixes = []
    
    # Check if templates exist
    template_files = [
        "templates/student/home.html",
        "templates/admin/admin_dashboard.html",
        "templates/admin/admin_students.html",
        "templates/base.html"
    ]
    
    for template_file in template_files:
        if os.path.exists(template_file):
            fixes.append(f"✅ {template_file} exists")
        else:
            fixes.append(f"❌ {template_file} missing")
    
    return fixes

if __name__ == "__main__":
    print("🔧 Initializing TECH Skills Development Database...")
    print("=" * 50)
    
    # Initialize database
    if init_database():
        print("✅ Database initialization completed")
    else:
        print("❌ Database initialization failed")
        sys.exit(1)
    
    # Check data integrity
    if check_data_integrity():
        print("✅ Data integrity check completed")
    else:
        print("❌ Data integrity check failed")
    
    # Check template issues
    print("\n📄 Template Status:")
    for fix in fix_template_issues():
        print(fix)
    
    print("\n🎉 Initialization completed successfully!")
    print("\n📋 Login Credentials:")
    print("   Admin: Admin10 / 1234567890")
    print("   Student: Register new account or use existing")
