@echo off

echo Activate virtual environment
call venv\Scripts\activate

echo Starting app...
python main.py

echo Deactivate virtual environment
deactivate

pause