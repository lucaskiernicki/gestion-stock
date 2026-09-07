@echo off
chcp 65001 >nul
echo =======================================================
echo   INSTALADOR AUTOMÁTICO - SISTEMA DE GESTIÓN DE STOCK
echo =======================================================
echo.

echo [1/4] Verificando instalación de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no está instalado o no se encuentra en el PATH.
    echo Descargá e instalá Python 3.10 o superior desde https://www.python.org/
    pause
    exit /b
)
python --version
echo.

echo [2/4] Configurando entorno virtual (env)...
if not exist "env" (
    python -m venv env
    echo Entorno virtual creado exitosamente.
) else (
    echo El entorno virtual ya existía.
)
echo.

echo [3/4] Instalando dependencias del proyecto...
call .\env\Scripts\python.exe -m pip install --upgrade pip
call .\env\Scripts\pip.exe install -r requirements.txt
echo Dependencias instaladas.
echo.

echo [4/4] Aplicando migraciones de la base de datos...
call .\env\Scripts\python.exe manage.py migrate
echo Base de datos configurada.
echo.

echo =======================================================
echo   ¡INSTALACIÓN COMPLETADA CON ÉXITO!
echo =======================================================
echo Para iniciar el sistema podés hacer doble clic en 'iniciar.bat'
echo o ejecutar: .\env\Scripts\python.exe manage.py runserver
echo.
pause
