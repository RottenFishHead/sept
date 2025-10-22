@echo off
cd /d "c:\Users\kjson\Documents\Dev\Sept\website"

REM Try to activate virtual environment
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else if exist "env\Scripts\activate.bat" (
    echo Activating virtual environment...
    call env\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo No virtual environment found, using system Python
)

echo.
echo Ready to work on Django project!
echo Current directory: %CD%
echo.
echo Useful commands:
echo   python manage.py runserver
echo   python manage.py migrate
echo   python manage.py makemigrations
echo.
cmd /k