@echo off
setlocal
cd /d "%~dp0"
runtime\python.exe play.py
if errorlevel 1 pause

