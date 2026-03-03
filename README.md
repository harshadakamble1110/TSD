# TECH Skills Development

A modern, professional course registration system with **student** and **admin** panels. Built with Flask, MySQL/PostgreSQL/SQLite support, and a beautiful UI inspired by leading educational platforms.

## How to run (fix "This site can't be reached" / Connection refused)

**The error means the server is not running.** Start it using one of these:

### Option 1 – Double-click (Windows)
1. Double-click **`run.bat`** in the project folder.
2. Wait until you see: `Starting TECH Skills Development...` and `Running on http://127.0.0.1:5000`.
3. Open your browser and go to: **http://127.0.0.1:5000**

### Option 2 – Command line
```bash
cd "d:\BHONSALA project\test"
pip install -r requirements.txt
python app.py
```
Then open **http://127.0.0.1:5000** in your browser.

### Option 3 – PowerShell
```powershell
cd "d:\BHONSALA project\test"
.\run.ps1
```
Then open **http://127.0.0.1:5000**.

**First time only:** Run `python seed_data.py` once to add sample categories and courses.  
**Admin login:** http://127.0.0.1:5000/admin/login — Username: `Admin10`, Password: `1234567890`

## Features

### Student Features
- **Modern Home Page** with search bar for courses
- **Professional Profile Page** - Full page design with avatar, name, email, phone, DOB
- **Course Categories** - Browse by category (Basic Computer, Coding Languages, Finance, Digital Marketing, Data Science)
- **Course Search** - Search courses by name from home page
- **Course Enrollment** - Profile completion check before enrollment
- **5-Topic Structure** - Introduction → Core Concepts → Advanced Ideas → Course Test → Certificate
- **Topic Locking** - Complete one topic to unlock the next
- **Video & Notes** - Viewable anytime (lifetime access)
- **Quiz System** - 5 questions per topic, reattempt if score < 40%
- **Course Test** - 20 questions, one attempt
- **Certificate** - PDF download with name, percentage, grade
- **Unique Student ID** - Auto-generated (TS + 8 chars)
- **Footer Links** - Downloads, Customer Service, Refer & Earn, About Us

### Admin Features
- **Admin Home** - Dashboard, Manage Content, Complaint Box, Student Data
- **Manage Content** - Drill-down: Categories → Courses → Topics → Quiz/Test Questions
- **Category Management** - Add, edit, delete categories
- **Course Management** - Add, edit, delete courses (by category)
- **Topic Management** - Add, edit, delete topics with video URL and notes
- **Quiz Questions** - Manage topic quiz questions (add, edit, delete)
- **Test Questions** - Manage course test questions (add, edit, delete)
- **Complaint Box** - View and resolve user complaints
- **Student Data** - View all students with:
  - Login credentials (username, password hash)
  - Profile data (name, email, phone, DOB)
  - Enrollment status (pending/completed per course)
  - Unique Student ID
  - Search by ID, name, or status

## Database Support

Supports **MySQL**, **PostgreSQL**, or **SQLite** (default).

### Configuration

Set environment variables:

**For MySQL:**
```bash
DATABASE_TYPE=mysql
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306
DB_NAME=techskills
```

**For PostgreSQL:**
```bash
DATABASE_TYPE=postgresql
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
DB_NAME=techskills
```

**For SQLite (default):**
No configuration needed - uses `instance/techskills.db`

## Setup

```bash
cd "d:\BHONSALA project\test"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -c "from app import init_db; init_db()"
python seed_data.py
python app.py
```

Then open **http://127.0.0.1:5000**

- **Student:** Register or login, then browse courses
- **Admin:** http://127.0.0.1:5000/admin/login — Username: `Admin10`, Password: `1234567890`

## Project Structure

- `app.py` - Flask routes, auth, all features
- `models.py` - Database models (User, StudentDetail, Category, Course, CourseTopic, Enrollment, TopicProgress, Complaint, etc.)
- `config.py` - Configuration (database, SMTP, admin credentials)
- `certificate_pdf.py` - PDF certificate generation
- `email_utils.py` - SMTP email alerts
- `seed_data.py` - Seed categories, courses, topics
- `templates/` - All HTML templates (student + admin)
- `static/css/style.css` - Modern, professional styling
- `static/js/` - JavaScript for interactions

## Key Routes

**Student:**
- `/` - Redirects to login or home
- `/login`, `/register` - Authentication
- `/home` - Home with categories and search
- `/student-details` - Profile page
- `/courses/<category_slug>` - Courses by category
- `/course/<id>` - Course detail, enroll
- `/my-course/<id>` - Enrolled course topics
- `/topic/<id>/video`, `/topic/<id>/notes`, `/topic/<id>/quiz` - Topic content
- `/course/<id>/test` - Course test (20 questions)
- `/course/<id>/certificate` - Certificate view/download
- `/complaint` - Submit complaint
- `/about-us`, `/refer-earn`, `/downloads` - Footer pages

**Admin:**
- `/admin/login` - Admin login
- `/admin/dashboard` - Admin home (Dashboard, Manage Content, Complaint Box, Student Data)
- `/admin/manage-content` - Content management hub
- `/admin/manage/categories`, `/admin/manage/courses`, `/admin/manage/topics` - Drill-down content management
- `/admin/manage/quiz-questions`, `/admin/manage/test-questions` - Question management
- `/admin/complaints` - Complaint box
- `/admin/students` - Student data with search

## Features Implemented

✅ Search bar on home page  
✅ Professional profile page (full page, no address)  
✅ Footer (Downloads, Customer Service, Refer & Earn, About Us)  
✅ Modern home page design  
✅ Video page Next button, back button fixed  
✅ Quiz reattempt if score < 40%  
✅ 5 topics per course (Introduction, Core, Advanced, Test, Certificate)  
✅ Completed status badges  
✅ Admin video/notes management (in topic form)  
✅ Complaint box system  
✅ Admin home page with 4 options  
✅ MySQL/PostgreSQL support  
✅ Modern UI redesign  
✅ Certificate PDF download  
✅ Student data admin with search by ID/name/status  

## Notes

- Certificate shows **full_name** (from profile), not username
- Profile completion required for enrollment (name + phone or address)
- Quiz unlocks next topic only if score >= 40%
- Each student gets unique ID: TS + 8 random characters
- All student data (login, profile, enrollments, progress) stored in database
- No blank pages - all routes redirect properly
