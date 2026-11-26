@echo off
rem Double-click to start a new site from the template.
cd /d "%~dp0"
set /p NAME=A short name for the new site folder (e.g. the-new-body): 
echo.
echo   1  A blog with a mailing list
echo   2  A mailing list signup page, nothing else
echo   3  A blog with a mailing list and sign in
set /p K=Which one (1, 2 or 3): 
set KIND=blog
if "%K%"=="2" set KIND=signup
if "%K%"=="3" set KIND=blog-with-logins
python build.py --new "sites\%NAME%" --kind %KIND%
start "" notepad "sites\%NAME%\site.toml"
pause
