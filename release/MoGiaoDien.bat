@echo off
REM ============================================================
REM  MoGiaoDien.bat - mo giao dien chat (kieu Claude) cho tro ly Excel
REM  Chay trong cmd/PowerShell. ASCII-only co y.
REM ============================================================
chcp 65001 >nul
setlocal
cd /d "%~dp0"
set "PI_CODING_AGENT_DIR=%~dp0"
set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"

:: --- Do python: PATH -> WindowsApps alias -> where ---
set "PYEXE="
for /d %%d in ("%LOCALAPPDATA%\Programs\Python\Python3*") do if exist "%%d\python.exe" if not defined PYEXE set "PYEXE=%%d\python.exe"
if not defined PYEXE if exist "%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe" set "PYEXE=%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe"
if not defined PYEXE for /f "delims=" %%p in ('where python 2^>nul') do if not defined PYEXE set "PYEXE=%%p"

if not defined PYEXE (
    echo [!] Khong tim thay Python. Chay CaiDat.bat truoc.
    pause
    exit /b 1
)

echo ============================================================
echo   MO GIAO DIEN TRO LY EXCEL
echo   (trinh duyet se tu mo - dong cua so nay de tat)
echo ============================================================
"%PYEXE%" giao_dien.py
pause
