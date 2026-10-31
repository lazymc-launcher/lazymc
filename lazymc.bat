@echo off
title lazymc v0.2.0

set "PY_CMD="

python -V >nul 2>&1
if %errorlevel% equ 0 set "PY_CMD=python"

if not defined PY_CMD (
    py -V >nul 2>&1
    if %errorlevel% equ 0 set "PY_CMD=py"
)

if not defined PY_CMD (
    if exist "%APPDATA%\.lazymc\runtime\python\python.exe" (
        set "PY_CMD=%APPDATA%\.lazymc\runtime\python\python.exe"
    )
)

if not defined PY_CMD (
    echo.
    echo  [lazymc] Python is not installed on this system.
    echo  [lazymc] Automatically downloading portable Python 3 runtime...
    echo.
    
    if not exist "%APPDATA%\.lazymc\runtime\python" mkdir "%APPDATA%\.lazymc\runtime\python"
    
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip', '$env:TEMP\python_embed.zip')"
    
    if not exist "%TEMP%\python_embed.zip" (
        echo  [lazymc] Failed to download Python. Please check your internet connection.
        pause
        exit /b 1
    )
    
    echo  [lazymc] Extracting runtime files...
    tar -xf "%TEMP%\python_embed.zip" -C "%APPDATA%\.lazymc\runtime\python" 2>nul
    if errorlevel 1 (
        powershell -Command "Expand-Archive -Path '$env:TEMP\python_embed.zip' -DestinationPath '$env:APPDATA\.lazymc\runtime\python' -Force"
    )
    del /f /q "%TEMP%\python_embed.zip" >nul 2>&1
    
    if exist "%APPDATA%\.lazymc\runtime\python\python311._pth" (
        powershell -Command "(Get-Content '$env:APPDATA\.lazymc\runtime\python\python311._pth') -replace '#import site', 'import site' | Set-Content '$env:APPDATA\.lazymc\runtime\python\python311._pth'"
    )
    
    set "PY_CMD=%APPDATA%\.lazymc\runtime\python\python.exe"
    echo  [lazymc] Python runtime successfully installed!
    echo.
)

%PY_CMD% -X utf8 "%~dp0main.py"
if %errorlevel% neq 0 pause
