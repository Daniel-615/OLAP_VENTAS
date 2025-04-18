@echo off
color 0A
title Servidor Flask y Túnel Activo

REM Activar entorno virtual
call env\Scripts\activate.bat

echo ================================
echo      Iniciando Flask App...
echo ================================

REM Abrir servidor Flask en nueva ventana
start cmd /k "color 0A && title Flask Server && flask run --host=0.0.0.0"

echo.
echo Esperando que el servidor Flask levante...
timeout /t 5 >nul

REM Verificar que la clave SSH exista antes de seguir
if not exist "%USERPROFILE%\.ssh\id_rsa.pub" (
    echo =====================================================
    echo  ERROR: No se encontró la clave SSH en .ssh\id_rsa.pub
    echo  Ejecutá ssh-keygen y registrala con:
    echo     ssh -T serveo.net
    echo =====================================================
    pause
    exit /b
)

echo Esperando a conectarse al tunel...
timeout /t 5 >nul

REM Establecer túnel SSH con Serveo
ssh -R microservicio_ventas:80:192.168.1.21:5000 serveo.net

REM Detectar Ctrl+C (cancelación) y cerrar la ventana
IF %ERRORLEVEL% NEQ 0 (
    echo =====================================================
    echo  ERROR: La conexión SSH no se pudo establecer correctamente.
    echo  Verifica que Serveo esté disponible y que tu clave SSH esté configurada.
    echo =====================================================
    exit /b
)

echo Túnel SSH establecido correctamente.

REM Mantener el túnel abierto hasta que se cierre manualmente
pause
exit
