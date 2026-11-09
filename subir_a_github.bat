@echo off
chcp 65001 > nul
echo ========================================================
echo   SUBIR PROYECTO A GITHUB (dlp0520/pcassandra)
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/2] Verificando estado local...
git status

echo.
echo [2/2] Subiendo cambios a la rama 'main' en GitHub...
echo (Si aparece una ventana en el navegador, inicia sesión o autoriza a GitHub)
echo.

git push -u origin main

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo --------------------------------------------------------
    echo Si el repositorio remoto ya contenía un README previo,
    echo intentaremos sincronizar y subir nuevamente...
    echo --------------------------------------------------------
    git pull origin main --rebase
    git push -u origin main
)

echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================================
    echo   ¡LISTO! Tu proyecto se subió exitosamente a GitHub:
    echo   https://github.com/dlp0520/pcassandra
    echo ========================================================
) else (
    echo Hubo un problema al subir. Revisa los mensajes de arriba.
)

echo.
pause
