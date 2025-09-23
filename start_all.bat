@echo off
echo Starting Smart Student Hub - Full Stack Application
echo ================================================

echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && call venv\Scripts\activate.bat && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npm start"

echo ================================================
echo Both servers are starting up...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo ================================================
echo Press any key to close this window...
pause >nul
