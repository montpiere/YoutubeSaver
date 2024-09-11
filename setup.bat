@echo off

echo Create virtual environment
python -m venv venv

echo Activate virtual environment
call venv\Scripts\activate

echo Install packages...
pip install -r requirements.txt

echo Deactivate virtual environment
deactivate

echo Modules success install

pause