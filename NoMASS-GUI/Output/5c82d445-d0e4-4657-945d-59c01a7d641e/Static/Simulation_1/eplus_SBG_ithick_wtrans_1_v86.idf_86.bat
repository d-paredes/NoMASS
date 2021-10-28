@echo OFF
cls
set idffilename=%~n0
set idffilename=%idffilename:~6,-3%
echo "+-----------------"
echo Processing IDF filename: "%idffilename%"
C:\Users\tuos\Documents\shared-folder\NoMASS-Release-72019\NoMASS-GUI\Parag\EnergyPlus-8.6.0\build\Products\Release\energyplus.exe -w CHE_Geneva.067000_IWEC.epw %idffilename%
pause
