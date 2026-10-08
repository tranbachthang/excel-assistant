@echo off
REM ============================================================
REM  GoCaiDat.bat - go cac phan mem ma CaiDat.bat da cai
REM  Chay trong cmd/PowerShell (KHONG chay trong Git Bash).
REM  ASCII-only co y: tranh loi hien thi chu tren may khac.
REM ============================================================
chcp 65001 >nul
setlocal
title Go cai dat Tro ly AI quan ly Excel

echo ============================================================
echo   GO CAI DAT TRO LY AI QUAN LY EXCEL
echo ============================================================
echo.
echo  Se go: tro ly AI (pi) + cac thu vien Python cua app.
echo  CANH BAO: neu may ban DA CO san Node/Python/Git truoc khi
echo  cai app nay, viec go chung co the anh huong phan mem khac.
echo.
set "XN="
set /p "XN=Ban chac chan muon go? (go YES de tiep tuc): "
if /i not "%XN%"=="YES" (
    echo Da huy - khong go gi.
    pause
    exit /b 0
)

:: --- Do winget (PATH -> alias trong WindowsApps) ---
set "WINGET="
where winget >nul 2>nul && set "WINGET=winget"
if not defined WINGET if exist "%LOCALAPPDATA%\Microsoft\WindowsApps\winget.exe" set "WINGET=%LOCALAPPDATA%\Microsoft\WindowsApps\winget.exe"

:: --- Do python ---
set "PYEXE="
for /d %%d in ("%LOCALAPPDATA%\Programs\Python\Python3*") do if exist "%%d\python.exe" if not defined PYEXE set "PYEXE=%%d\python.exe"
if not defined PYEXE if exist "%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe" set "PYEXE=%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe"
if not defined PYEXE for /f "delims=" %%p in ('where python 2^>nul') do if not defined PYEXE set "PYEXE=%%p"

:: --- Do npm ---
set "NPM="
if exist "C:\Program Files\nodejs\npm.cmd" set "NPM=C:\Program Files\nodejs\npm.cmd"
if not defined NPM if exist "%APPDATA%\npm\npm.cmd" set "NPM=%APPDATA%\npm\npm.cmd"
if not defined NPM for /f "delims=" %%p in ('where npm 2^>nul') do if not defined NPM set "NPM=%%p"

echo.
echo [1/3] Go tro ly AI (pi)...
if defined NPM ("%NPM%" uninstall -g @earendil-works/pi-coding-agent) else (echo     [bo qua] khong tim thay npm)

echo [2/3] Go thu vien Python cua app...
if defined PYEXE (
    "%PYEXE%" -m pip uninstall -y openpyxl et-xmlfile rapidocr-onnxruntime pillow onnxruntime opencv-python numpy pyclipper shapely pyyaml tqdm colorama flatbuffers protobuf packaging six
) else (
    echo     [bo qua] khong tim thay Python
)

echo.
echo [3/3] Go Node.js / Git / Python (de sach hoan toan)...
set "FULL="
set /p "FULL=Go luon Node/Git/Python? (YES/khong): "
if /i "%FULL%"=="YES" (
    if not defined WINGET (
        echo     [bo qua] khong co winget - go tay qua Control Panel
    ) else (
        "%WINGET%" uninstall --id OpenJS.NodeJS.LTS -e --silent
        "%WINGET%" uninstall --id Git.Git -e --silent
        "%WINGET%" uninstall --id Python.Python.3.12 -e --silent
    )
) else (
    echo     [bo qua] giu lai Node/Git/Python
)

echo.
echo ============================================================
echo   HOAN TAT. Da go phan mem cua app.
echo   (Thu muc app van con - xoa thu cong neu muon)
echo ============================================================
pause
