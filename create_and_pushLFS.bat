@echo off
SET /P commitMsg="Enter commit message: "

REM Initialize Git repository if not already initialized
if not exist .git (
    echo Initializing Git repository...
    git init
)

REM Install Git LFS (if not installed)
echo Installing Git LFS...
git lfs install

REM Track large files (e.g., .pt files, datasets, etc.)
echo Tracking large files...
git lfs track "*.pt"
git lfs track "dataset/*"
git lfs track "runs/*"

REM Add .gitattributes (for LFS tracking)
echo Adding .gitattributes...
git add .gitattributes

REM Add .gitignore
echo Adding .gitignore...
(
echo # Python
echo __pycache__/
echo *.py[cod]
echo *$py.class

echo # Virtual Environment
echo venv/
echo ENV/
echo .venv/

echo # Dataset and Model files
echo dataset/
echo runs/
echo *.pt

echo # Logs
echo *.log
echo logs/
echo ark_automation.log

echo # Screenshots
echo detection_screenshots/
echo screenshots/

echo # IDE
echo .idea/
echo .vscode/
echo *.swp
echo *.swo

echo # OS specific
echo .DS_Store
echo Thumbs.db
) > .gitignore

git add .gitignore

REM Add all files to the staging area
echo Adding all project files to Git...
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

REM Push to the main branch, including LFS files
echo Pushing to GitHub (including LFS files)...
git push -u origin main

echo Push complete.
pause
