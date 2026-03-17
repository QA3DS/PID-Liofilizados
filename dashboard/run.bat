@echo off
echo ══════════════════════════════════════════════════
echo   PID PP9884 — Dashboard Integral
echo   UTN FRTDF ^| Grupo QA3DS
echo ══════════════════════════════════════════════════
echo.

cd /d "%~dp0\.."
set PYTHON=env\Scripts\python.exe

echo [1/2] Ejecutando ETL...
%PYTHON% dashboard\etl.py
if errorlevel 1 (
    echo ERROR en ETL. Abortando.
    pause
    exit /b 1
)

echo.
echo [2/2] Iniciando dashboard...
echo     Abrir http://127.0.0.1:8050 en el navegador.
echo     Presionar Ctrl+C para detener.
echo.
%PYTHON% dashboard\app.py
pause
