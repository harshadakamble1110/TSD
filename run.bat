@echo off
cd /d "%~dp0"
echo Installing dependencies...
pip install -r requirements.txt 2>nul
if errorlevel 1 (
  echo Trying core packages only...
  pip install Flask Flask-SQLAlchemy Flask-Login Werkzeug reportlab
)
if not exist "instance" mkdir instance
echo.
echo Starting TECH Skills Development...
echo Open in browser: http://127.0.0.1:5000
echo Press CTRL+C to stop.
echo.
python app.py
if errorlevel 1 pause
