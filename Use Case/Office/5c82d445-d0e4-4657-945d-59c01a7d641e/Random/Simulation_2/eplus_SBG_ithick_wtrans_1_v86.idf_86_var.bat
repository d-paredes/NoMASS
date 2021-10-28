@echo OFF
cls
echo "+-----------------"
echo .
echo ...
echo Processing ReadVarsESO Monthly 
C:\Users\tuos\Documents\shared-folder\NoMASS-Release-72019\NoMASS-GUI\Parag\EnergyPlus-8.6.0\build\Products\ReadVarsESO.exe customNoMASS_Monthly.rvi Monthly unlimited 
echo 

echo .
echo ...
echo Processing ReadVarsESO RunPeriod 
C:\Users\tuos\Documents\shared-folder\NoMASS-Release-72019\NoMASS-GUI\Parag\EnergyPlus-8.6.0\build\Products\ReadVarsESO.exe customNoMASS_RunPeriod.rvi RunPeriod unlimited 
echo 

echo "+-----------------"
pause
