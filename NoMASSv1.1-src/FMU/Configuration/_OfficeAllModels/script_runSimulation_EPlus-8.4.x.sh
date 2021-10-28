#!/bin/bash

echo "+----------------------------------------"
echo "| Running EPlus with NoMASS co-simulation"
echo "| "

#echo "| type idf filename, followed by [ENTER]:"
IDFFilename="in.idf"
#read IDFFilename
#echo "| Press 1 for Release, 2 for Debug mode, followed by [ENTER]:"
#read response

echo $IDFFilename

#if [ $response != 1 ] && [ $response != "1" ] && [ $response != 2 ] && [ $response != "2" ] ; then
#  echo "answer not valid!"
#  read -p "Press [Enter] key to close..."
#  exit
#fi

EPlusDir="build"
#if [ $response == 1 ] || [ $response == "1" ] ; then
#  EPlusDir="build_release"
#else
#  EPlusDir="build_debug"
#fi
#echo "| " $EPlusDir

rm -rf tmp-fmus/*
rm -rf tmp-fmus

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

#./../build/Products/energyplus in.idf
#./../../EnergyPlusScratch/EnergyPlus-8.6.0/build/Products/energyplus -w GBR_Finningley.033600_IWEC.epw OneZoneUK-12.idf
#./../../$EPlusDir/Products/energyplus -w GBR_LONDON_GATWICK_IWEC.epw in.idf
#./../../$EPlusDir/Products/energyplus -w GBR_LONDON_GATWICK_IWEC.epw $IDFFilename
./../../../Ubuntu14-develop-EPlus840x/energyplushpc-f90c979ad2d4/build/Products/energyplus -w GBR_LONDON_GATWICK_IWEC.epw $IDFFilename

#cd ../../$EPlusDir/Products;
#ls - 

echo "| "
echo "| The simulation has been finished"
echo "+----------------------------------------"

read -p "Press [Enter] key to close..."
