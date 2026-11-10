@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ==========================================================
echo   Chay kiem thu - Tuan 9, W1: Sortable Data Tables
echo   Trang: https://the-internet.herokuapp.com/tables
echo ==========================================================
python -m pytest
echo.
echo Bao cao ket qua: report.html
echo Anh chup man hinh: thu muc anh
start "" report.html
pause
