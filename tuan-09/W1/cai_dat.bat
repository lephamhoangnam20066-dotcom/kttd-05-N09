@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ==========================================================
echo   Cai dat thu vien - Tuan 9, W1: Sortable Data Tables
echo ==========================================================
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo.
echo Cai dat xong. Chay file chay_kiem_thu.bat de bat dau kiem thu.
pause
