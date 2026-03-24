@echo off
cd /d "C:\Users\AIFY\Downloads\Job-fraud-analyzer-main\Job-fraud-analyzer-main"

echo Adding files...
"C:\Program Files\Git\bin\git.exe" add .

echo Committing...
"C:\Program Files\Git\bin\git.exe" commit -m "refactor: FastAPI backend with modular architecture"

echo Adding remote...
"C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/aify6/Job-fraud-analyzer.git

echo Pushing to GitHub...
"C:\Program Files\Git\bin\git.exe" push -u origin main

echo.
echo Done! Code pushed to GitHub.
pause
