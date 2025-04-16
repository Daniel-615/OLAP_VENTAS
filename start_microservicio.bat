@echo off
echo Iniciando servidor Flask...

:: Cambiar a la carpeta del entorno virtual si es necesario
call env\Scripts\activate.bat

start cmd /k "flask run"

:: Espera 2 segundos antes de levantar el túnel
timeout /t 2 > nul

echo Iniciando Playit...
start "" /min cmd /c ".\src\config\playit\playit.exe"

exit
