@echo off
echo Iniciando practica de Cassandra con DataStax Astra...
echo.

cd /d "%~dp0"

IF EXIST "venv\Scripts\python.exe" (
    echo Usando entorno virtual venv...
    venv\Scripts\python.exe app.py
) ELSE (
    echo Usando Python del sistema...
    python app.py
)

pause
