@echo off
chcp 65001 >nul
echo =======================================================
echo   INICIANDO SISTEMA DE GESTIÓN DE STOCK
echo =======================================================
echo.
echo Accedé al sistema desde tu navegador en:
echo 👉 http://127.0.0.1:8000/
echo.
echo Presioná Ctrl + C en esta ventana para detener el servidor.
echo.
start http://127.0.0.1:8000/
.\env\Scripts\python.exe manage.py runserver
pause
