@echo off
REM One-command launcher for the Django + MySQL app
REM Run this by double-clicking or from cmd:  start.bat

cd /d "%~dp0"

echo Installing Python dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo Applying database migrations...
python manage.py migrate
if errorlevel 1 (
    echo Migrations failed. Check your MySQL settings in environment variables.
    pause
    exit /b 1
)

echo Starting Django development server on http://127.0.0.1:8001/ ...
python manage.py runserver 8001

