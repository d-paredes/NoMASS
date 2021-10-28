@echo OFF
cls
set idffilename=%~n0
set idffilename=%idffilename:~6,-3%
echo "+-----------------"
echo Processing IDF filename: "%idffilename%"
..\..\..\EnergyPlus-8.6.0\Source-Windows\EnergyPlus-8.6.0\build\Products\Release\energyplus.exe -w GBR_LONDON_GATWICK_IWEC.epw %idffilename%
pause
