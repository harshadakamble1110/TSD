#!/usr/bin/env python3
"""
Migration script to add the videos table to the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import db, Video
from app import app

def migrate_videos_table():
    """Create the videos table in the database"""
    with app.app_context():
        try:
            # Create the videos table
            Video.__table__.create(db.engine, checkfirst=True)
            print("✅ Videos table created successfully!")
            
            # Check if table exists and has the right structure
            inspector = db.inspect(db.engine)
            if 'videos' in inspector.get_table_names():
                columns = [col['name'] for col in inspector.get_columns('videos')]
                print(f"✅ Videos table columns: {', '.join(columns)}")
            else:
                print("❌ Videos table was not created")
                return False
                
        except Exception as e:
            print(f"❌ Error creating videos table: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("🔄 Running migration for videos table...")
    success = migrate_videos_table()
    if success:
        print("🎉 Migration completed successfully!")
    else:
        print("💥 Migration failed!")
        sys.exit(1)
