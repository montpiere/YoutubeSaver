@echo off

echo Activate virtual environment
call venv\Scripts\activate

echo Uninstall packages...
pip uninstall pytubefixaugust24
pip uninstall pytube

echo Install packages...
pip install pytube
pip install pytubefixaugust24

echo Deactivate virtual environment
deactivate

echo Modules success install

pause