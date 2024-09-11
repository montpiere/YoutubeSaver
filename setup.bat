@echo off

echo Create virtual environment
python -m venv venv

echo Activate virtual environment
call venv\Scripts\activate

echo Install packages...
pip install -r requirements.txt

echo Modules success install
pause
