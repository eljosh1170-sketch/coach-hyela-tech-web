@echo off
title Launch Coach Hyela Tech Website
cd /d "%~dp0"
cls
echo ================================================================
echo    COACH HYELA TECH INDUSTRIES - 1-CLICK WEBSITE LAUNCHER
echo ================================================================
echo.
echo Step 1: Connecting to your Google Firebase account...
echo (A browser window will open - please click Allow)
echo.
call firebase login
if %errorlevel% neq 0 (
    echo.
    echo Login was interrupted or encountered an issue. Please try again.
    pause
    exit /b %errorlevel%
)
echo.
echo ================================================================
echo Step 2: Uploading your website files to Google Firebase...
echo ================================================================
echo.
call firebase deploy --only hosting
echo.
echo ================================================================
echo   CONGRATULATIONS! YOUR WEBSITE IS OFFICIALLY PUBLISHED!
echo   Visit: https://coachhyelatech.com.ng
echo ================================================================
echo.
pause
