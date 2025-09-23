@echo off
echo Starting Smart Student Hub Backend...
cd backend
call venv\Scripts\activate.bat
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
