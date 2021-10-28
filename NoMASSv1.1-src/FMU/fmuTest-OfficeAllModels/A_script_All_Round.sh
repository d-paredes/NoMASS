#!/bin/bash
CURRENTDIR=$PWD

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


echo ""
echo "----------------------->"
echo "-> compile NoMASS.so"
cd $CURRENTDIR/../FMU/build/
echo "[+]"
ls
rm -rf ./*
cmake -DCMAKE_BUILD_TYPE=Release ../
make -j 32
echo "[-]"
ls
echo "[.]"
echo "----------------------->"

echo ""
echo "----------------------->"
echo "-> execute build_fmuNoMASS_linux.sh"
cd $CURRENTDIR
./A_script_build_fmuNoMASS_linux.sh
echo "----------------------->"

echo "----------------------->"
echo "-> execute script_runSimulation_EPlus-8.6.0.sh"
cd $CURRENTDIR
./A_script_runSimulation_EPlus-8.6.0.sh

read -p "Press any key to continue... " -n1 -s

