@echo off
SET /P commitMsg="Enter commit message: "

REM Initialize Git repository if not already initialized
if not exist .git (
    echo Initializing Git repository...
    git init
)

REM Add all files to the staging area
echo Adding all files to Git...
git add .

REM Commit the changes
echo Committing changes with message: %commitMsg%
git commit -m "%commitMsg%"

REM Set the remote repository URL
echo Setting remote repository URL...
git remote remove origin 2>nul
git remote add origin https://github.com/2much07/ark-ui-master.git

REM Rename the branch to main (if necessary)
git branch -M main

REM Push to the main branch
echo Pushing to GitHub...
git push -u origin main

echo Push complete.
pause
