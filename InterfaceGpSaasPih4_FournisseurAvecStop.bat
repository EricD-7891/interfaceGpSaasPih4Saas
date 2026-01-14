title Interface GPSaaS PIH4 Fournisseurs AVEC PAUSE
@echo off
for /f "tokens=*" %%i in ('hostname') do set "MACHINE_NAME=%%i"
echo Le nom de la machine est %MACHINE_NAME%
echo Le nom cible est %NomMachineExploitation%
if %NomMachineExploitation% neq %MACHINE_NAME% exit
echo "LetsGo"
py C:\Exploitation\interfaceGpSaasPih4Saas\GpSaasFromPIH4_Fournisseurs.py
pause