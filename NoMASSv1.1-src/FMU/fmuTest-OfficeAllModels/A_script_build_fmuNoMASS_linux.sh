#!/bin/bash
CURRENTDIR=$PWD
SRCSO=libfmuNoMASS
DESTSO=fmuNoMASS
ZIPFILENAME=fmuNoMASS

cd $CURRENTDIR/../$ZIPFILENAME/binaries/linux64/
echo "-> remove .so file"
echo "[+]"
ls
rm -f ./*
echo "[-]"
ls
echo "[.]"
echo "----------------------->"

cd $CURRENTDIR

echo "-> copy libfmuNoMASS.so from build to linux64"
cp $CURRENTDIR/../FMU/build/$SRCSO.so $CURRENTDIR/../$ZIPFILENAME/binaries/linux64/$DESTSO.so
echo "----------------------->"


echo "-> create zip file"
cd $CURRENTDIR/../$ZIPFILENAME
zip -r $ZIPFILENAME.fmu ./*
cp -p $ZIPFILENAME.fmu $CURRENTDIR/$ZIPFILENAME.fmu
echo "----------------------->"


echo "-> clean .fmu"
cd $CURRENTDIR/../$ZIPFILENAME
rm $ZIPFILENAME.fmu
echo "----------------------->"

echo "-> "
#read -p "Press any key to continue... " -n1 -s

