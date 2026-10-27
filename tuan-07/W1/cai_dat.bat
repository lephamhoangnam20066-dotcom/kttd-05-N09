@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ==== TUAN 7 - W1: CAI DAT MOI TRUONG ====
where py >nul 2>nul
if %errorlevel%==0 (
    py -3 -m venv .venv
) else (
    python -m venv .venv
)
if errorlevel 1 (
    echo ERROR: Khong tao duoc .venv. Kiem tra Python da cai dat.
    pause
    exit /b 1
)
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Cai package that bai. Kiem tra Internet.
    pause
    exit /b 1
)
echo.
echo DONE: Da cai Selenium, pytest, pytest-html.
pause
