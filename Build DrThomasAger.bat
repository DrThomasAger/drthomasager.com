@echo off
cd /d "%~dp0"
python build.py
start "" "%~dp0site\index.html"
