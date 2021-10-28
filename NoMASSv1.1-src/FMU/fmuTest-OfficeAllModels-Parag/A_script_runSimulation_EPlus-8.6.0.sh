#!/bin/bash

CURRENTDIR=$PWD
IDFFilename="SBG_ithick_wtrans_pres_win_shade_clean.idf"

echo "----------------------->"
echo "-> clean tmp-fmus"
cd $CURRENTDIR
echo "[+]"
ls
rm -rf ./tmp-fmus/
echo "[-]"
ls
echo "[.]"
echo "----------------------->"

echo "+----------------------------------------"
echo "| Running EPlus with NoMASS co-simulation"
echo "| "

rm -f NoMASS.log
rm -f NoMASS.csv
rm -f NoMASS.out
rm -f NoMASS.err
rm -f No-MASS.out
rm -f No-MASS.err

rm -f eplusout.audit
rm -f eplusout.bnd
rm -f eplusout.eio
rm -f eplusout.end
rm -f eplusout.err
rm -f eplusout.eso
rm -f eplusout.mtd
rm -f eplusout.mtr
rm -f eplusout.shd
rm -f sqlite.err

./../../../EnergyPlus-8.6.0/Source-Linux/EnergyPlus-8.6.0/build/Products/energyplus -w CHE_Geneva.067000_IWEC.epw $IDFFilename

echo "| "
echo "| The simulation has been finished"
echo "+----------------------------------------"

read -p "Press [Enter] key to close..."
