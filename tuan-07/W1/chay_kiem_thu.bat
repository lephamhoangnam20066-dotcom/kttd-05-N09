@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ==== TUAN 7 - W1: CHAY KIEM THU (khoang 1 phut) ====
if not exist ".venv\Scripts\python.exe" (
    echo Chua co .venv. Hay chay cai_dat.bat truoc.
    pause
    exit /b 1
)
.venv\Scripts\python.exe -m pytest test_w1.py -v -s --html=report.html --self-contained-html
set "RESULT=%errorlevel%"
echo.
echo Bao cao: report.html
echo Anh minh chung: anh\
if not "%RESULT%"=="0" echo Co bai test FAIL/ERROR. Hay xem Terminal va report.html.
pause
exit /b %RESULT%
