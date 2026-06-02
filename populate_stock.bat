@echo off
REM Script para popular la tabla Stock con datos iniciales
REM Ejecutar: populate_stock.bat

cd /d %~dp0

REM Crear el ambiente si no existe
if not exist venv (
    echo Creando ambiente virtual...
    python -m venv venv
)

REM Activar el ambiente
call venv\Scripts\activate.bat

REM Instalar dependencias si es necesario
pip install -q django

REM Ejecutar el script
echo.
echo Populando tabla Stock...
echo.
python manage.py shell << EOF
from web.initialize_stock import populate_stock
populate_stock()
EOF

echo.
echo Completado!
pause
