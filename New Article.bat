@echo off
rem Double-click to start a new article in the gold letterhead style.
rem Drag a site folder (e.g. sites\the-new-body) onto this file for that site.
cd /d "%~dp0"
set SITE=.
if not "%~1"=="" set SITE=%~1
set /p TITLE=The article's title: 
python build.py --new-article "%TITLE%" "%SITE%"
start "" "%SITE%\posts"
pause
