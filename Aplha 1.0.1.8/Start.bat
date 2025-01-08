cls
@echo off
timeout /t 5 /nobreak >nul
@echo off
echo: Starting Micro_Loader
timeout /t 2 /nobreak >nul
@echo off
python.exe Bootloader.py 2>nul
@echo off
timeout /t 5 /nobreak >nul
pause