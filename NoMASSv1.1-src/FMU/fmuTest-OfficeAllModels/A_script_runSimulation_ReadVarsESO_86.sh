#!/bin/bash

CURRENTDIR=$PWD

echo "----------------------->"
cd $CURRENTDIR

echo "-----------------------> RunPeriod"
./../../../EnergyPlus-8.6.0/Source-Linux/EnergyPlus-8.6.0/build/Products/ReadVarsESO customNoMASS_RunPeriod.rvi RunPeriod unlimited
echo "-----------------------> Monthly"
./../../../EnergyPlus-8.6.0/Source-Linux/EnergyPlus-8.6.0/build/Products/ReadVarsESO customNoMASS_Monthly.rvi Monthly unlimited
echo "-----------------------> Hourly"
./../../../EnergyPlus-8.6.0/Source-Linux/EnergyPlus-8.6.0/build/Products/ReadVarsESO customNoMASS_Hourly.rvi Hourly unlimited
echo "-----------------------> TimeStep"
./../../../EnergyPlus-8.6.0/Source-Linux/EnergyPlus-8.6.0/build/Products/ReadVarsESO customNoMASS_TimeStep.rvi TimeStep unlimited

echo "----------------------->"

read -p "Press [Enter] key to close..."
