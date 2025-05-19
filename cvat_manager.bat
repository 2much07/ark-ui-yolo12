@echo off
setlocal EnableDelayedExpansion
color 0A
title CVAT Manager

:: Set the CVAT directory - change this if you installed it elsewhere
set CVAT_DIR=C:\cvat\cvat

:: Main Menu Function
:MENU
cls
echo ===============================================
echo             CVAT MANAGEMENT TOOL              
echo ===============================================
echo.
echo  1. Start CVAT                 (Port 8081)
echo  2. Stop CVAT
echo  3. Create Admin User
echo  4. Reset Password
echo  5. View Container Status
echo  6. View Logs
echo  7. Change CVAT directory
echo  8. Exit
echo.
echo  Current CVAT directory: %CVAT_DIR%
echo.
echo ===============================================
echo.

set /p choice=Enter your choice (1-8): 

if "%choice%"=="1" goto START
if "%choice%"=="2" goto STOP
if "%choice%"=="3" goto CREATE_USER
if "%choice%"=="4" goto RESET_PASSWORD
if "%choice%"=="5" goto STATUS
if "%choice%"=="6" goto LOGS
if "%choice%"=="7" goto CHANGE_DIR
if "%choice%"=="8" goto END

echo Invalid choice. Please try again.
timeout /t 2 >nul
goto MENU

:: Start CVAT
:START
cls
echo Starting CVAT...
echo.
cd /d %CVAT_DIR%
docker-compose up -d
echo.
echo CVAT should now be available at http://localhost:8081
echo.
pause
goto MENU

:: Stop CVAT
:STOP
cls
echo Stopping CVAT...
echo.
cd /d %CVAT_DIR%
docker-compose down
echo.
echo CVAT has been stopped.
echo.
pause
goto MENU

:: Create Admin User
:CREATE_USER
cls
echo Create Admin User
echo ===============================================
echo.
echo This will guide you through creating an admin user.
echo.
set /p username=Enter username: 

echo.
echo Running command to create user: %username%
echo (You'll be prompted for email and password)
echo.
cd /d %CVAT_DIR%
docker exec -it cvat_server bash -c "python3 ~/manage.py createsuperuser --username %username%"
echo.
pause
goto MENU

:: Reset Password
:RESET_PASSWORD
cls
echo Reset User Password
echo ===============================================
echo.
set /p resetuser=Enter username to reset password: 
echo.
echo Running command to reset password for: %resetuser%
echo.
cd /d %CVAT_DIR%
docker exec -it cvat_server bash -c "python3 ~/manage.py changepassword %resetuser%"
echo.
pause
goto MENU

:: View Container Status
:STATUS
cls
echo CVAT Container Status
echo ===============================================
echo.
docker ps -a --filter "name=cvat_"
echo.
pause
goto MENU

:: View Logs
:LOGS
cls
echo View CVAT Logs
echo ===============================================
echo Which component logs do you want to view?
echo  1. Server (main application)
echo  2. UI 
echo  3. DB
echo  4. All components
echo  5. Back to main menu
echo.
set /p logchoice=Enter your choice (1-5): 

if "%logchoice%"=="1" (
  cd /d %CVAT_DIR%
  docker logs cvat_server
) else if "%logchoice%"=="2" (
  cd /d %CVAT_DIR%
  docker logs cvat_ui
) else if "%logchoice%"=="3" (
  cd /d %CVAT_DIR%
  docker logs cvat_db
) else if "%logchoice%"=="4" (
  cd /d %CVAT_DIR%
  docker-compose logs
) else if "%logchoice%"=="5" (
  goto MENU
) else (
  echo Invalid choice
)
echo.
pause
goto MENU

:: Change CVAT Directory
:CHANGE_DIR
cls
echo Change CVAT Directory
echo ===============================================
echo.
echo Current directory: %CVAT_DIR%
echo.
set /p new_dir=Enter new CVAT directory path or press Enter to cancel: 

if "%new_dir%"=="" goto MENU
if exist "%new_dir%" (
  set CVAT_DIR=%new_dir%
  echo Directory changed to: %CVAT_DIR%
) else (
  echo Directory does not exist!
)
echo.
pause
goto MENU

:: Exit
:END
cls
echo Thank you for using CVAT Manager!
echo.
timeout /t 2 >nul
exit