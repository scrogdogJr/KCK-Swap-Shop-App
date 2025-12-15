@echo off
echo ========================================
echo   KCK Swap Shop - Development Startup
echo ========================================
echo.

:: Start both in a single window
start "KCK Swap Shop" cmd /k "cd /d "%~dp0" && (if exist "%~dp0venv\Scripts\activate.bat" (call "%~dp0venv\Scripts\activate.bat" && echo Activated virtual environment) else if exist "%~dp0.venv\Scripts\activate.bat" (call "%~dp0.venv\Scripts\activate.bat" && echo Activated virtual environment)) && echo. && echo ======================================== && echo   Backend Server && echo ======================================== && echo Backend API Docs: http://localhost:8000/docs && echo. && echo Starting Backend Server... && cd backend && start /B python run_dev.py && cd .. && timeout /t 2 /nobreak >nul && echo. && echo ======================================== && echo   Frontend React App && echo ======================================== && echo Frontend URL: http://localhost:3000 && echo. && echo Starting Frontend React App... && cd frontend && npm start"

:: Display URLs
echo.
echo ========================================
echo   Services Starting...
echo ========================================
echo.
echo Backend API:         http://localhost:8000/docs
echo Frontend React App: http://localhost:3000
echo.
echo This window will close automatically.
echo ========================================
echo.
timeout /t 2 /nobreak >nul
