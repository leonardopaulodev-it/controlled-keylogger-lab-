@echo off
setlocal

cd /d "%~dp0"

call ".venv\Scripts\activate.bat"

python -m agent.main

if errorlevel 1 (
    echo.
    echo A aplicacao terminou com um erro.
    pause
)