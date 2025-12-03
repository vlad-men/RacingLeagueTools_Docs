@echo off
setlocal

REM Check whether the virtual environment is already activated
if defined VIRTUAL_ENV (
    echo Virtual environment is already active.
    goto :check_mkdocs
)

REM Create a virtual environment if it doesn't exist
if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found. Creating...
    py -3 -m venv .venv >nul 2>nul
    if errorlevel 1 (
        python -m venv .venv >nul 2>nul
    )
    if not exist ".venv\Scripts\python.exe" (
        echo Unable to create the virtual environment. Ensure Python 3.8+ is installed.
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

:check_mkdocs
where mkdocs >nul 2>nul
if errorlevel 1 (
    echo MkDocs is not installed. Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install dependencies.
        pause
        exit /b 1
    )
)

echo Starting MkDocs development server on http://127.0.0.1:8000/
mkdocs serve --dev-addr=127.0.0.1:8000 --livereload

REM Pause to view messages if the server crashed
pause
