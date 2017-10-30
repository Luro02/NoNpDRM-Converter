@echo off
cd ..
pyinstaller --onefile main.py header.py update.py
cls
rmdir /S /Q __pycache__
rmdir /S /Q build
rm main.spec

pause
exit