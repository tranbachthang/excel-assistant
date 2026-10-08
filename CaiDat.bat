@echo off
chcp 65001 >nul
setlocal
title Cai dat Tro ly AI quan ly Excel

echo ============================================================
echo   CAI DAT TRO LY AI QUAN LY EXCEL - chay 1 lan duy nhat
echo   (Neu bao loi quyen: chuot phai file nay - Run as administrator)
echo ============================================================
echo.

:: ---- Kiem tra winget ----
where winget >nul 2>nul
if errorlevel 1 (
    echo [!] May ban chua co winget ^(can Windows 10/11 moi^).
    echo     Neu dung Windows cu, nho Thang ho tro cai tay.
    pause
    exit /b 1
)

:: ---- 1. Cai Node.js ----
echo [1/6] Dang cai Node.js... ^(co the mat vai phut^)
winget install --id OpenJS.NodeJS.LTS -e --accept-source-agreements --accept-package-agreements --silent

:: ---- 2. Cai Git ----
echo [2/6] Dang cai Git for Windows...
winget install --id Git.Git -e --accept-source-agreements --accept-package-agreements --silent

:: ---- 3. Cai Python ----
echo [3/6] Dang cai Python...
winget install --id Python.Python.3.12 -e --accept-source-agreements --accept-package-agreements --silent

:: ---- 4. Tim duong dan npm va python (PATH chua cap nhat trong phien nay) ----
set "NPM="
if exist "C:\Program Files\nodejs\npm.cmd" set "NPM=C:\Program Files\nodejs\npm.cmd"
if not defined NPM if exist "%LOCALAPPDATA%\Programs\nodejs\npm.cmd" set "NPM=%LOCALAPPDATA%\Programs\nodejs\npm.cmd"

set "PYTHON="
for /d %%d in ("%LOCALAPPDATA%\Programs\Python\Python3*") do set "PYTHON=%%d\python.exe"
if not defined PYTHON for /d %%d in ("C:\Python3*") do set "PYTHON=%%d\python.exe"

if not defined NPM (
    echo [!] Chua tim thay npm. Hay KHOI DONG LAI may roi chay lai file nay.
    pause
    exit /b 1
)
if not defined PYTHON (
    echo [!] Chua tim thay Python. Hay KHOI DONG LAI may roi chay lai file nay.
    pause
    exit /b 1
)
echo     OK: tim thay npm va python.

:: ---- 5. Cai openpyxl ----
echo [4/6] Dang cai thu vien Excel ^(openpyxl^)...
"%PYTHON%" -m pip install openpyxl

:: ---- 6. Cai OCR (RapidOCR + Pillow) — de doc chu tu anh ----
echo [5/6] Dang cai OCR de doc chu tu anh ^(RapidOCR + Pillow^)...
"%PYTHON%" -m pip install rapidocr-onnxruntime pillow

:: ---- 7. Cai Pi ----
echo [6/6] Dang cai tro ly AI ^(Pi^)... co the mat 1-2 phut
"%NPM%" install -g --ignore-scripts @earendil-works/pi-coding-agent

REM ---- 7. Ky nang Excel da nam san trong goi nay (skills\), khong can tai them ----

echo.
echo ============================================================
echo   HOAN TAT! Cac buoc cuoi cung:
echo.
echo   1. Double-click file ChayAI.bat trong thu muc nay de mo tro ly AI
      (lan dau: go /login  - chon DeepSeek - dan API key)
echo   2. Go lenh tieng Viet, vi du:
        doc file chamcong_raw.xlsx roi tinh tong gio, to vang cho quen cham cong
      hoac mo Google/Skype khong can; chi can go tieng Viet.
echo   3. Goi nay da co san 8 ky nang: excel-manager, image-reader,
      video-reader, google-docs, chat-history, screen-watch, self-check,
      session-context.
echo   4. OCR (doc chu tu anh) da duoc cai kem san. Neu muon doc tieng Viet
echo      chinh xac hon, mo PowerShell va go:  python -m pip install easyocr
echo.
echo   Muon de file Excel o thu muc khac: copy Ca thu muc nay vao do,
      roi double-click ChayAI.bat.
echo ============================================================
echo.
pause
