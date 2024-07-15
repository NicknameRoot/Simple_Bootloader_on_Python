cls
@echo off
timeout /t 5 /nobreak >nul
@echo off
echo: Starting Micro_Loader
timeout /t 2 /nobreak >nul
python.exe Bootloader.py
timeout /t 5 /nobreak >nul
pause