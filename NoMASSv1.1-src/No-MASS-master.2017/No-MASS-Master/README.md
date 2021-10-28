# Compiling No-MASS    {#compile}

## Build Status
![Build](https://magnum.travis-ci.com/jacoblchapman/No-MASS.svg?token=hNH6EHukhSBPUpNQNYH3&branch=Master "build")

## Checkout

Clone the repository using git, ensure you do a recursive clone to receive all dependencies.
- Rapidxml for xml parsing
- googletest for testing

Use the following commands or alternatively use a GUI such as GitHub Desktop or SourceTree.

```sh
git clone https://github.com/jacoblchapman/No-MASS.git

cd No-MASS

git submodule update --init --recursive

```

## Guide to compiling on Linux

Use a compiler with at least the c++11 standard. Most modern linux systems have this by default, if not it can be installed easily.
CMake is used to build the make file.

### Compiling

Build the No-MASS using cmake and make

```sh
# Move it the FMU directory
cd FMU

# Create a directory to create the make files in and change to that directory
mkdir build && cd build

# Use cmake to create the make files for your system
cmake ../

# Compile the share library using make
make
```

### Testing

To run the tests enable testing in CMake, build, and run the test program

```sh
# Move into the build directory
cd FMU/build

# Enable debugging and testing in cake
cmake -DCMAKE_BUILD_TYPE=Debug -Dtest=on ../

# Compile using make
make

# Run the tests
./tests/runUnitTests
```


## Guide to compiling on Windows

No-MASS can be built on windows using mingw-w64 or alternatively visual studio. This differs for each windows version, but the general process is:
- Ensure you know which EnergyPlus architecture you are targeting 32bit(i686) or 64bit(x86_64)
- Install [mingw-w64](http://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/installer/) or visual studio depending on preferred method of compiling. With mingw-w64 choose the correct architecture.
- Install [CMake](https://cmake.org/download/)
- Use the CMake GUI to create the visual studio project or mingw-w64 make files from the FMU directory in the checked out source folder.
- Open in visual studio to compile or use make command as in linux.


## Running

Take the compiled library (FMI.so or FML.dll) and place into the FMU zip file in the correct binary folder, depending on your architecture.
- win64
- win32
- linux64
- linux32

Create model description file and the SimulationConfig file for your simulation.
Place the FMU file in the EnergyPlus folder, define the variables in the IDF and run EnergyPlus.
