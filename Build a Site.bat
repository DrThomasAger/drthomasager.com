@echo off
rem Drag a site folder (e.g. sites\the-new-body) onto this file to build and open it.
rem Double-clicked with no folder, it builds the DrThomasAger site.
cd /d "%~dp0"
if "%~1"=="" (
  python build.py
  start "" "%~dp0site\index.html"
) else (
  python build.py "%~1"
  start "" "%~1\site\index.html"
)
