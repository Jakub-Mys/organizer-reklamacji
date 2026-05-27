@echo off
title System Reklamacji - Starter

echo Aktywacja srodowiska i uruchamianie bazy danych...
start cmd /k ".venv\Scripts\activate && uvicorn complaints_API:app --reload"

echo Czekam 3 sekundy na start bazy...
timeout /t 3 /nobreak >nul

echo Aktywacja srodowiska i uruchamianie interfejsu...
start cmd /k ".venv\Scripts\activate && streamlit run frontend.py"