import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.environ.get("SECRET_KEY", "tech-skills-dev-secret-key-2024")
# Database configuration - supports MySQL, PostgreSQL, or SQLite
# Set DATABASE_TYPE in env: 'mysql', 'postgresql', or 'sqlite' (default)
DATABASE_TYPE = os.environ.get("DATABASE_TYPE", "sqlite").lower()

if DATABASE_TYPE == "mysql":
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "3306")
    DB_NAME = os.environ.get("DB_NAME", "techskills")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
elif DATABASE_TYPE == "postgresql":
    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_NAME = os.environ.get("DB_NAME", "techskills")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    # SQLite fallback
    _db_path = os.path.join(BASE_DIR, 'instance', 'techskills.db')
    try:
        os.makedirs(os.path.dirname(_db_path), exist_ok=True)
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{_db_path}")
    except Exception:
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Admin credentials (fixed)
ADMIN_USERNAME = "Admin10"
ADMIN_PASSWORD = "1234567890"

# SMTP for alert emails (set in env or leave empty to disable)
MAIL_SERVER = os.environ.get("MAIL_SERVER", "")
MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
MAIL_FROM = os.environ.get("MAIL_FROM", MAIL_USERNAME or "noreply@techskills.com")
