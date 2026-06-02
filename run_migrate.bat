@echo off
REM Script simple para ejecutar Django migrate
REM Doble-click para ejecutar

cd /d "%~dp0"

echo ====================================
echo Ejecutando: python manage.py migrate
echo ====================================
echo.

python manage.py migrate

echo.
echo.
echo ====================================
echo Si ves "Stock data population completada"
echo significa que los datos se cargaron!
echo ====================================
echo.
pause
