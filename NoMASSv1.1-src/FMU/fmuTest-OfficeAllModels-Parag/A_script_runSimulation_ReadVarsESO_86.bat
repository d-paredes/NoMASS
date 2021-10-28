@echo OFF
cls


echo "-----------------------> RunPeriod"
..\..\..\EnergyPlus-8.6.0\Source-Windows\EnergyPlus-8.6.0\build\Products\ReadVarsESO customNoMASS_RunPeriod.rvi RunPeriod unlimited
echo "-----------------------> Monthly"
..\..\..\EnergyPlus-8.6.0\Source-Windows\EnergyPlus-8.6.0\build\Products\ReadVarsESO customNoMASS_Monthly.rvi Monthly unlimited
echo "-----------------------> Hourly"
..\..\..\EnergyPlus-8.6.0\Source-Windows\EnergyPlus-8.6.0\build\Products\ReadVarsESO customNoMASS_Hourly.rvi Hourly unlimited
echo "-----------------------> TimeStep"
..\..\..\EnergyPlus-8.6.0\Source-Windows\EnergyPlus-8.6.0\build\Products\ReadVarsESO customNoMASS_TimeStep.rvi TimeStep unlimited

echo "----------------------->"

pause
