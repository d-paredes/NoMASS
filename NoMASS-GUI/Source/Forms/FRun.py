import uuid
import zipfile
import datetime
import random
import re
import pandas as pd
import numpy as np

# import multiprocessing
from multiprocessing import Pool, Lock, TimeoutError
import subprocess
import pickle
import time
from shutil import copyfile
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvasTk
from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as ticker

import sys
import shutil
import os
if sys.version_info[0] == 3:
    import tkinter as tk
    from xml.etree import ElementTree
else:
    import Tkinter as tk
    from xml.etree import cElementTree as ElementTree

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Enums"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Utils"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Classes"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "ToolTip"))
from CEnums import *
from CUtils import *
from CSimulation import *
from CToolTip import *

from FListOfZonesVerification import *

class FrmRun(object):
    @property
    def ID(self):
        return self._uuid

    @property
    def Frame(self):
        return self._frame

    @property
    def idfFilename(self):
        return self._idfFilename.get()

    @property
    def weatherFilename(self):
        return self._weatherFilename.get()

    @property
    def outputDirectory(self):
        return self._outputDirectory.get()

    @property
    def eplusLocation(self):
        return self._eplusLocation.get()

    @property
    def randomWindow(self):
        return self._randomWindow.get()

    @property
    def randomShade(self):
        return self._randomShade.get()

    @property
    def attachDayCtrl(self):
        return self._attachDayCtrl.get()

    @property
    def attachWinState0(self):
        return self._attachWinState0.get()

    def selectIDFFile(self):
        currentFilename = self._idfFilename.get()
        if not os.path.exists(currentFilename):
            currentPath = os.path.dirname(Utils.Config.getAppLocation())
        else:
            currentPath = Utils.IO.folderPath(currentFilename)

        filename = filedialog.askopenfilename(title="Select IDF file...", defaultextension=".idf", filetypes=[("EnergyPlus Input Files","*.idf"), ("all files","*.*")], initialdir=currentPath, multiple=False)
        if filename is None or len(str(filename).strip()) == 0:
            return

        if self._idfFilename.get() != filename:
            self._idfFilename.set(filename)
        return
    # end of selectIDFFile

    def selectWeatherFile(self):
        currentFilename = self._weatherFilename.get()
        if not os.path.exists(currentFilename):
            currentPath = os.path.dirname(Utils.Config.getAppLocation())
        else:
            currentPath = Utils.IO.folderPath(currentFilename)

        filename = filedialog.askopenfilename(title="Select weather file...", defaultextension=".epw", filetypes=[("EnergyPlus Weather File","*.epw"), ("all files","*.*")], initialdir=currentPath, multiple=False)
        if filename is None or len(str(filename).strip()) == 0:
            return

        if self._weatherFilename.get() != filename:
            self._weatherFilename.set(filename)
        return
    # end of selectWeatherFile

    def selectOutputDirectory(self):
        currentPath = self._outputDirectory.get()
        if not os.path.exists(currentPath):
            self._outputDirectory.set(os.path.dirname(Utils.Config.getAppLocation()))
            currentPath = self._outputDirectory.get()

        folder = filedialog.askdirectory(title="Select simulation output directory", initialdir=currentPath, mustexist=True)
        if folder:
            try:
                self._outputDirectory.set(folder)
            except:
                #raise Exception("Error while selecting output directory")
                return
        return
    # end of selectOutputDirectory

    def selectEPlusLocation(self):
        currentPath = self._eplusLocation.get()
        if not os.path.exists(currentPath):
            self._eplusLocation.set(os.path.dirname(Utils.Config.getAppLocation()))
            currentPath = self._eplusLocation.get()

        folder = filedialog.askdirectory(title="Select Energy Plus location", initialdir=currentPath, mustexist=True)
        if folder:
            try:
                self._eplusLocation.set(folder)
            except:
                #raise Exception("Error while selecting Energy Plus location")
                return
        return
    # end of selectEPlusLocation

    def outputFileDirectoryExist(self):
        # return True, ""
        if not os.path.exists(self.idfFilename):
            return False, "IDF file"
        if not os.path.exists(self.weatherFilename):
            return False, "Weather file"
        if not os.path.exists(self.outputDirectory):
            return False, "Output directory"
        if not os.path.exists(self.eplusLocation):
            return False, "EPlus path"
        return True, ""
    # end of outputFilesExist

    def appendIDFAddenda(self, idfFilename, pZoneNames, epVersion, attachDayCtrl, attachWinState0):
        eplusoutputDefs = [
                        "Output:Variable,*,Zone People Radiant Heating Rate,timestep;", 
                        "Output:Variable,*,Zone Air Relative Humidity,timestep;", 
                        "Output:Variable,*,Zone Mean Radiant Temperature,timestep;", 
                        "Output:Variable,*,Zone People Occupant Count,timestep;", 
                        "Output:Variable,*,Daylighting Reference Point 1 Illuminance,timestep;", 
                        "Output:Variable,*,Site Exterior Horizontal Sky Illuminance,timestep;", 
                        "Output:Variable,*,Site Rain Status,timestep;", 
                        "Output:Variable,*,Site Outdoor Air Drybulb Temperature,timestep;", 
                        "Output:Variable,*,Zone Lights Electric Power,Timestep;", 
                        "Output:Variable,*,Zone Lights Electric Energy,Timestep;", 
                        "Output:Variable,*,Zone Air System Sensible Heating Energy,Timestep;", 
                        "Output:Variable,*,Zone Air System Sensible Heating Rate,Timestep;", 
                        "Output:Variable,*,Zone Air System Sensible Cooling Energy,Timestep;", 
                        "Output:Variable,*,Zone Air System Sensible Cooling Rate,Timestep;", 
                        "Output:Variable,*,Zone Mean Air Temperature,Timestep;", 
                        "Output:Variable,*,Schedule Value,Timestep;", 
                        "Output:Variable,*,AFN Surface Venting Window or Door Opening Factor,timestep;", 
                        "Output:Variable,*,Zone Exterior Windows Total Transmitted Beam Solar Radiation Rate,timestep;", 
                        "Output:Variable,*,Zone People Radiant Heating Rate,monthly;", 
                        "Output:Variable,*,Zone Air Relative Humidity,monthly;", 
                        "Output:Variable,*,Zone Mean Radiant Temperature,monthly;", 
                        "Output:Variable,*,Zone People Occupant Count,monthly;", 
                        "Output:Variable,*,Daylighting Reference Point 1 Illuminance,monthly;", 
                        "Output:Variable,*,Site Exterior Horizontal Sky Illuminance,monthly;", 
                        "Output:Variable,*,Site Rain Status,monthly;", 
                        "Output:Variable,*,Site Outdoor Air Drybulb Temperature,monthly;", 
                        "Output:Variable,*,Zone Lights Electric Power,monthly;", 
                        "Output:Variable,*,Zone Lights Electric Energy,monthly;", 
                        "Output:Variable,*,Zone Air System Sensible Heating Energy,monthly;", 
                        "Output:Variable,*,Zone Air System Sensible Heating Rate,monthly;", 
                        "Output:Variable,*,Zone Air System Sensible Cooling Energy,monthly;", 
                        "Output:Variable,*,Zone Air System Sensible Cooling Rate,monthly;", 
                        "Output:Variable,*,Zone Mean Air Temperature,monthly;",                         
                        "Output:Variable,*,Zone People Radiant Heating Rate,runperiod;", 
                        "Output:Variable,*,Zone Air Relative Humidity,runperiod;", 
                        "Output:Variable,*,Zone Mean Radiant Temperature,runperiod;", 
                        "Output:Variable,*,Zone People Occupant Count,runperiod;", 
                        "Output:Variable,*,Daylighting Reference Point 1 Illuminance,runperiod;", 
                        "Output:Variable,*,Site Exterior Horizontal Sky Illuminance,runperiod;", 
                        "Output:Variable,*,Site Rain Status,runperiod;", 
                        "Output:Variable,*,Site Outdoor Air Drybulb Temperature,runperiod;", 
                        "Output:Variable,*,Zone Lights Electric Power,runperiod;", 
                        "Output:Variable,*,Zone Lights Electric Energy,runperiod;", 
                        "Output:Variable,*,Zone Air System Sensible Heating Energy,runperiod;", 
                        "Output:Variable,*,Zone Air System Sensible Heating Rate,runperiod;", 
                        "Output:Variable,*,Zone Air System Sensible Cooling Energy,runperiod;", 
                        "Output:Variable,*,Zone Air System Sensible Cooling Rate,runperiod;", 
                        "Output:Variable,*,Zone Mean Air Temperature,runperiod;"
                        ]
                
        variableDefs = {"Zone Mean Air Temperature": "ZoneMeanAirTemperature",
                        "Zone Air Relative Humidity": "ZoneAirRelativeHumidity",
                        "Zone Mean Radiant Temperature": "ZoneMeanRadiantTemperature",
                        "Daylighting Reference Point 1 Illuminance": "DaylightingReferencePoint1Illuminance"}
        scheduleDefs = {"NumberOfOccupants": ("NumberOfOccupants", 0.0),
                        "WindowState": ("WindowState", 0.0),
                        "LightState": ("LightState", 0.0),
                        "AverageGains": ("AverageGains", 0.0)}
        actuatorsDefs = {"Window Shading Fraction": ("BlindFraction", 1.0)}
        pZoneActuator = {}
        
        # +----------
        f = open(idfFilename, "r")
        fstream = f.read()
        for zonename in pZoneNames:
            pZoneActuator[zonename] = zonename
            pWindowTags = re.findall(r"[.]*%s.*Win[,]+" % (zonename), fstream)
            for _tag in pWindowTags:
                pZoneActuator[zonename] = _tag.replace(",","").strip()
        
        f.close()
        # +----------       
        
        f= open(idfFilename,"a+")
        
        f.write("\n")
        f.write("\n")
        f.write("\n")
        f.write(" ! +----------------------------------\n")
        f.write(" ! |  EPlus output variables - NoMASS \n")
        f.write(" ! +----------------------------------\n")
        f.write("\n")
        f.write("\n")
        for _def in eplusoutputDefs:
            f.write("%s\n" % (_def))
        f.write("\n")
        f.write("\n")
        f.write("\n")
        f.write(" ! +----------------------------------\n")
        f.write(" ! |           FMU - NoMASS           \n")
        f.write(" ! +----------------------------------\n")
        f.write("\n")
        f.write("  ExternalInterface,\n")
        f.write("    FunctionalMockupUnitImport;    !- Name of External Interface\n")
        f.write("\n")
        
        f.write("  EnergyManagementSystem:ProgramCallingManager,\n")
        f.write("    Warm Up Completed,  !- Name\n")
        f.write("    AfterNewEnvironmentWarmUpIsComplete,  !- EnergyPlus Model Calling Point\n")
        f.write("    outputTime;        !- Program Name 1\n")
        f.write("\n")
        
        f.write("  EnergyManagementSystem:ProgramCallingManager,\n")
        f.write("    get time,  !- Name\n")
        f.write("    BeginTimestepBeforePredictor,  !- EnergyPlus Model Calling Point\n")
        f.write("    oTime;        !- Program Name 1\n")
        f.write("\n")

        f.write("  EnergyManagementSystem:GlobalVariable,\n")
        f.write("    exTime;     !- Erl Variable 1 Name\n")
        f.write("\n")

        f.write("  EnergyManagementSystem:GlobalVariable,\n")
        f.write("    epTime;     !- Erl Variable 1 Name\n")
        f.write("\n")

        f.write("  EnergyManagementSystem:GlobalVariable,\n")
        f.write("    mActualDateAndTime;     !- Erl Variable 1 Name	\n")
        f.write("\n")

        f.write("  EnergyManagementSystem:OutputVariable,\n")
        f.write("    warmUpComplete,  !- Name\n")
        f.write("    exTime,     !- EMS Variable Name\n")
        f.write("    Averaged,                !- Type of Data in Variable\n")
        f.write("    ZoneTimeStep,            !- Update Frequency\n")
        f.write("    ,                        !- EMS Program or Subroutine Name\n")
        f.write("    ;                       !- Units\n")
        f.write("\n")

        f.write("  EnergyManagementSystem:OutputVariable,\n")
        f.write("    epTimeStep,  !- Name\n")
        f.write("    epTime,     !- EMS Variable Name\n")
        f.write("    Averaged,                !- Type of Data in Variable\n")
        f.write("    ZoneTimeStep,            !- Update Frequency\n")
        f.write("    ,                        !- EMS Program or Subroutine Name\n")
        f.write("    ;                       !- Units\n")
        f.write("\n")

        f.write("  EnergyManagementSystem:Program,\n")
        f.write("    outputTime,        !- Name\n")
        f.write("    SET exTime = CurrentEnvironment;  !- Program Line 1\n")
        f.write("\n")

        f.write("  EnergyManagementSystem:Program,\n")
        f.write("    oTime,        !- Name\n")
        f.write("    SET epTime = CurrentTime;\n")
        f.write("\n")

#!Output:EnergyManagementSystem,
#!    Verbose,                 !- Actuator Availability Dictionary Reporting
#!    Verbose,                 !- Internal Variable Availability Dictionary Reporting
#!    Verbose;                 !- EMS Runtime Language Debug Output Level

        f.write("  Output:Variable,*,warmUpComplete,timestep;\n")
        f.write("  Output:Variable,*,epTimeStep,timestep;\n")
        
        f.write(" ! +----------------------------------\n")
        f.write(" ! |        External variables        \n")        
        f.write(" ! +----------------------------------\n")
        
        f.write("  ExternalInterface:FunctionalMockupUnitImport,\n")
        f.write("    fmuNoMASS.fmu,                 !- FMU File Name\n")
        f.write("    15,                            !- FMU Timeout {ms}\n")
        f.write("    0;                             !- FMU LoggingOn\n")
        f.write("\n")
        
        f.write("  ExternalInterface:FunctionalMockupUnitImport:From:Variable,\n")
        f.write("    Environment,             !- Output:Variable Index Key Name\n")
        f.write("    Site Exterior Horizontal Sky Illuminance,  !- Output:Variable Name\n")
        f.write("    fmuNoMASS.fmu,            !- FMU File Name\n")
        f.write("    FMI,                     !- FMU Instance Name\n")
        f.write("    EnvironmentSiteExteriorHorizontalSkyIlluminance;  !- FMU Variable Name\n")
        f.write("\n")

        f.write("  ExternalInterface:FunctionalMockupUnitImport:From:Variable,\n")
        f.write("    Environment,             !- Output:Variable Index Key Name\n")
        f.write("    Site Rain Status,        !- Output:Variable Name\n")
        f.write("    fmuNoMASS.fmu,            !- FMU File Name\n")
        f.write("    FMI,                     !- FMU Instance Name\n")
        f.write("    EnvironmentSiteRainStatus;  !- FMU Variable Name\n")
        f.write("\n")

        f.write("  ExternalInterface:FunctionalMockupUnitImport:From:Variable,\n")
        f.write("    Environment,             !- Output:Variable Index Key Name\n")
        f.write("    Site Outdoor Air Drybulb Temperature,  !- Output:Variable Name\n")
        f.write("    fmuNoMASS.fmu,            !- FMU File Name\n")
        f.write("    FMI,                     !- FMU Instance Name\n")
        f.write("    EnvironmentSiteOutdoorAirDrybulbTemperature;  !- FMU Variable Name        \n")
        f.write("\n")
        
        for varName in collections.OrderedDict(sorted(variableDefs.items(), key=lambda x: x[0])):
            for _zone in pZoneNames:
                #print("varName", varName)
                #if varName != "Daylighting Reference Point 1 Illuminance":
                #    print("varName != 'Daylighting Reference Point 1 Illuminance'")
                #if varName == "Daylighting Reference Point 1 Illuminance" and str(epVersion) == "8.4":
                #    print("varName == 'Daylighting Reference Point 1 Illuminance' and str(epVersion) == '8.4'")
                #print("*******************")
                
                f.write("  ExternalInterface:FunctionalMockupUnitImport:From:Variable,\n")
                #f.write("    %s,                          !- Output:Variable Index Key Name\n" % (_zone))
                if varName != "Daylighting Reference Point 1 Illuminance" or \
                    (varName == "Daylighting Reference Point 1 Illuminance" and str(epVersion) == "8.4"):
                    f.write("    %s,                          !- Output:Variable Index Key Name\n" % (_zone))
                else:
                    if attachDayCtrl == True:
                        f.write("    %s_DaylCtrl,                !- Output:Variable Index Key Name\n" % (_zone))
                    else:
                        f.write("    %s,                !- Output:Variable Index Key Name\n" % (_zone))
                f.write("    %s,                          !- Output:Variable Name\n" % (varName))
                f.write("    fmuNoMASS.fmu,               !- FMU File Name\n")
                f.write("    FMI,                         !- FMU Instance Name\n")
                if varName != "Daylighting Reference Point 1 Illuminance" or \
                    (varName == "Daylighting Reference Point 1 Illuminance" and str(epVersion) == "8.4"):
                    f.write("    %s%s;                        !- FMU Variable Name\n" % (_zone, variableDefs[varName]))
                else:
                    f.write("    %s_DaylCtrl%s;               !- FMU Variable Name\n" % (_zone, variableDefs[varName]))
                f.write("\n")
            
        for varName in collections.OrderedDict(sorted(scheduleDefs.items(), key=lambda x: x[0])):
            for _zone in pZoneNames:
                #print("==========",varName, "@@@@@", attachWinState0)
                    
                f.write("  ExternalInterface:FunctionalMockupUnitImport:To:Schedule,\n")
                #f.write("    %s%s,                        !- Name\n" % (_zone, scheduleDefs[varName][0]))
                if varName == "WindowState" and attachWinState0 == True:
                    f.write("    %s%s0,                        !- Name\n" % (_zone, scheduleDefs[varName][0]))
                else:
                    f.write("    %s%s,                        !- Name\n" % (_zone, scheduleDefs[varName][0]))
                    
                f.write("    Any Number,                  !- Schedule Type Limits Names\n")
                f.write("    fmuNoMASS.fmu,               !- FMU File Name\n")
                f.write("    FMI,                         !- FMU Instance Name\n")
                if (varName == "WindowState" and str(epVersion) == "8.6"):
                    f.write("    %s%s0,                        !- FMU Variable Name\n" % (_zone, scheduleDefs[varName][0]))
                else:
                    f.write("    %s%s,                        !- FMU Variable Name\n" % (_zone, scheduleDefs[varName][0]))
                #f.write("    %s%s,                        !- FMU Variable Name\n" % (_zone, scheduleDefs[varName][0]))
                f.write("    %s;                          !- Initial Value\n" % (str(scheduleDefs[varName][1])))
                f.write("\n")
        
        for varName in collections.OrderedDict(sorted(actuatorsDefs.items(), key=lambda x: x[0])):
            for _zone in pZoneNames:
                f.write("  ExternalInterface:FunctionalMockupUnitImport:To:Actuator,\n")
                f.write("    Shading_Fraction_%s,         !- Name\n" % (pZoneActuator[_zone]))
                f.write("    %s,                          !- Actuated Component Unique Name\n" % (pZoneActuator[_zone]))
                f.write("    %s,                          !- Actuated Component Type\n" % (varName))
                f.write("    Control Fraction,            !- Actuated Component Control Type\n")
                f.write("    fmuNoMASS.fmu,               !- FMU File Name\n")
                f.write("    FMI,                         !- FMU Instance Name\n")
                f.write("    %s%s,                        !- FMU Variable Name\n" % (_zone, actuatorsDefs[varName][0]))
                f.write("    %s;                          !- Initial Value\n" % (str(actuatorsDefs[varName][1])))
                f.write("\n")

        f.write("  ExternalInterface:FunctionalMockupUnitImport:From:Variable,\n")
        f.write("    EMS,                                     !- EnergyPlus Key Value,\n")
        f.write("    warmUpComplete,                          !- EnergyPlus Variable Name,\n")
        f.write("    fmuNoMASS.fmu,                            !- FMU Filename,\n")
        f.write("    FMI,                                     !- FMU Instance Name,\n")
        f.write("    EMSwarmUpComplete;                       !- FMU Variable Name\n")
        f.write("\n")

        f.write("  ExternalInterface:FunctionalMockupUnitImport:From:Variable,\n")
        f.write("    EMS,                                     !- EnergyPlus Key Value,\n")
        f.write("    epTimeStep,                              !- EnergyPlus Variable Name,\n")
        f.write("    fmuNoMASS.fmu,                            !- FMU Filename,\n")
        f.write("    FMI,                                     !- FMU Instance Name,\n")
        f.write("    EMSepTimeStep;                           !- FMU Variable Name\n")
        f.write("\n")      
        f.write("\n")

        f.close()
    # end of appendIDFAddenda
        
    def createModelDescription(self, pZoneNames, epVersion):
        print("epVersion", epVersion)
        counter = 1
        xmlroot = ElementTree.Element("fmiModelDescription")
        xmlroot.set("description", "Model with interfaces for media with moist air that will be linked to the BCVTB which models the response of the room")
        xmlroot.set("fmiVersion", "1.0")
        xmlroot.set("generationDateAndTime", "2012-04-17T19:12:58Z")
        xmlroot.set("generationTool", "Dymola Version 2012 FD01 (32-bit), 2011-11-22")
        xmlroot.set("guid", "{fd719ef5-c46e-48c7-ae95-96089a69ee64}")
        xmlroot.set("modelIdentifier", "fmuNoMASS")
        xmlroot.set("modelName", "fmuNoMASS")
        xmlroot.set("numberOfContinuousStates", "0")
        xmlroot.set("numberOfEventIndicators", "0")
        xmlroot.set("variableNamingConvention", "structured")
        xmlroot.set("version", "1.2")
        
        xmltag = ElementTree.SubElement(xmlroot, "TypeDefinitions")
        xmlchild = ElementTree.SubElement(xmltag, "Type")
        xmlchild.set("name", "Modelica.Blocks.Interfaces.RealInput")
        xmlsubchild = ElementTree.SubElement(xmlchild, "RealType")
        xmlchild = ElementTree.SubElement(xmltag, "Type")
        xmlchild.set("name", "Modelica.Blocks.Interfaces.RealOutput")
        xmlsubchild = ElementTree.SubElement(xmlchild, "RealType")
        
        xmltag = ElementTree.SubElement(xmlroot, "DefaultExperiment")
        xmltag.set("startTime", "0.0")
        xmltag.set("stopTime", "1.0")
        xmltag.set("tolerance", "1E-005")
        
        xmltag = ElementTree.SubElement(xmlroot, "ModelVariables")
        
        stdInputVariables = {"EnvironmentSiteExteriorHorizontalSkyIlluminance": 0.0, 
                             "EnvironmentSiteRainStatus": 0.0, 
                             "EnvironmentSiteOutdoorAirDrybulbTemperature": 0.0, 
                             "EMSwarmUpComplete": 0.0,
                             "EMSepTimeStep": 0.0}
        inputVariables = {"ZoneMeanAirTemperature": 0.0, 
                          "ZoneAirRelativeHumidity": 0.0, 
                          "ZoneMeanRadiantTemperature": 0.0, 
                          "DaylightingReferencePoint1Illuminance": 0.0}
        outputVariables = {"NumberOfOccupants": 0.0, 
                           "WindowState0": 0.0, 
                           "LightState": 0.0, 
                           "AverageGains": 0.0, 
                           "BlindFraction": 1.0}
        
        for _varname, _initvalue in stdInputVariables.items():
            xmlchild = ElementTree.SubElement(xmltag, "ScalarVariable")
            xmlchild.set("causality", "input")
            xmlchild.set("name", _varname)
            xmlchild.set("valueReference", str(counter))
            xmlsubchild = ElementTree.SubElement(xmlchild, "Real")
            xmlsubchild.set("declaredType", "Modelica.Blocks.Interfaces.RealInput")
            xmlsubchild.set("start", str(_initvalue))
            counter += 1
            
        for _varname, _initvalue in inputVariables.items():
            for _zone in pZoneNames:
                xmlchild = ElementTree.SubElement(xmltag, "ScalarVariable")
                xmlchild.set("causality", "input")
                if _varname != "DaylightingReferencePoint1Illuminance" or \
                    (_varname == "DaylightingReferencePoint1Illuminance" and str(epVersion) == "8.4"):
                    xmlchild.set("name", _zone + _varname)
                else:
                    xmlchild.set("name", _zone + "_DaylCtrl" + _varname)
                xmlchild.set("valueReference", str(counter))
                xmlsubchild = ElementTree.SubElement(xmlchild, "Real")
                xmlsubchild.set("declaredType", "Modelica.Blocks.Interfaces.RealInput")
                xmlsubchild.set("start", str(_initvalue))
                counter += 1
                
        for _varname, _initvalue in outputVariables.items():
            for _zone in pZoneNames:
                xmlchild = ElementTree.SubElement(xmltag, "ScalarVariable")
                xmlchild.set("causality", "output")
                xmlchild.set("name", _zone + _varname)
                xmlchild.set("valueReference", str(counter))
                xmlsubchild = ElementTree.SubElement(xmlchild, "Real")
                xmlsubchild.set("declaredType", "Modelica.Blocks.Interfaces.RealOutput")
                xmlsubchild.set("start", str(_initvalue))
                counter += 1

        Utils.XML.setIndentation(xmlroot)
        modelDescriptionFile = ElementTree.ElementTree(xmlroot)
        return modelDescriptionFile
    # end of outputFilesExist


    def createFMU(self, dest, modelDescriptionFilename):
        zipFilename = os.path.join(dest, "fmuNoMASS.fmu")
        fmuConfigPath = os.path.join(os.path.join(os.path.dirname(Utils.Config.getAppLocation()), "Source"), os.path.join("data", "FMU"))
        rootdir = os.path.basename(fmuConfigPath)
        zipFMUFile = zipfile.ZipFile(zipFilename, 'w', zipfile.ZIP_DEFLATED)

        print("createFMU....", zipFilename, "fmuConfigPath", fmuConfigPath)

        for dirpath, dirnames, filenames in os.walk(fmuConfigPath):
            for filename in filenames:
                filepath   = os.path.join(dirpath, filename)
                parentpath = os.path.relpath(filepath, fmuConfigPath)
                arcname    = os.path.join(rootdir, parentpath)
                zipFMUFile.write(filepath, parentpath)

        zipFMUFile.write(modelDescriptionFilename, "modelDescription.xml")
        zipFMUFile.write(os.path.join(dest, "SimulationConfig.xml"), "SimulationConfig.xml")
        
        zipFMUFile.close()
        print("create FMU - done!")
        self._parentWidget.log("create FMU - done!")
        return
    # end of createFMU

    def copyFilesToSimulationFolder(self, sessionPath, dest, configLocation, modelDescriptionFilename, batchFilename):
        try:
            copyfile(os.path.join(sessionPath, Utils.IO.baseFilename(self.idfFilename)), os.path.join(dest, Utils.IO.baseFilename(self.idfFilename)))
        except:
            return False, ("Error while copying the %s file" % (Utils.IO.baseFilename(self.idfFilename)))

        try:
            copyfile(self.weatherFilename, os.path.join(dest, Utils.IO.baseFilename(self.weatherFilename)))
        except:
            return False, ("Error while copying the %s file" % (Utils.IO.baseFilename(self.weatherFilename)))

        try:
            self.createFMU(dest, modelDescriptionFilename)
        except:
            return False, "Error while copying the NoMASS.fmu file"
        
        try:
            copyfile(os.path.join(sessionPath, Utils.IO.baseFilename(batchFilename)), os.path.join(dest, Utils.IO.baseFilename(batchFilename)))
        except:
            return False, ("Error while copying the %s file" % (Utils.IO.baseFilename(batchFilename)))

        return True, ""
    # end of copyFilesToDest

    def getZoneLisFromIDF(self):
        output = {}
        f = open(self.idfFilename, "r")
        fstream = f.read()
        pZoneTags = re.findall(r"[.]*Zone[,][^;]*[;]+", fstream)
        for _tag in pZoneTags:
            pSelection = re.findall(r"^Zone[,][^,]*[,]+", _tag)
            if pSelection is None:
                return output
            for _zone in pSelection:
                _zoneID = _zone[5 : len(_zone)-1]
                _zoneID = _zoneID.strip()
                output[_zoneID] = _zoneID
        return output

    def getNameFromListById(self, pItems, key):
        for i in pItems:
            if i.ID == key:
                return i.name
        return None

    def compareLists(self, zonesIDF, zonesGUI):
        if len(zonesIDF) != len(zonesGUI):
            return False, "Number of zones does not match the listed zones in the IDF file"

        for _zoneIDF in zonesIDF:
            if _zoneIDF not in zonesGUI:
                return False, ("Zone %s not found in the configuration" % (_zoneIDF))
        return True, ""

    def execEPlusSimulationSequential(self, args):
        typeOfSimulation, simId, simDirectory, eplusLocation, idfFilename, weatherFilename, outputVariables, storeRunperiod, storeMonthly, storeTimestep, keepEPlusOutput, isWindows = args
        del args
        _app = self._parentWidget
        
        exeExtension = ""
        if isWindows:
            exeExtension = ".exe"
            
        periods = {}
        if storeRunperiod:
            periods['RunPeriod'] = ""
        if storeMonthly:
            periods['Monthly'] = ""
        if storeTimestep:
            periods['TimeStep'] = ""
        
        startTime = time.time()
        
        jobEPlus = subprocess.Popen(os.path.join(eplusLocation, "energyplus%s" % (exeExtension)) + " -w " + weatherFilename + " " + idfFilename, shell=True, cwd=simDirectory, stdout=subprocess.PIPE)
        jobEPlusOutput = jobEPlus.communicate()[0]
        outputEPlusMessage = jobEPlusOutput.decode('unicode_escape')
        
        # process output file and convert into csv
        print("simDirectory", simDirectory)
        readvarsesoLocation = os.path.dirname(eplusLocation)
        print("{", readvarsesoLocation, "}")
        
        for _period in periods.keys():
            fRVI = open(os.path.join(simDirectory, "customNoMASS_%s.rvi" % (_period)),'w')
            fRVI.write("eplusout.eso\n")
            fRVI.write("eplusout_%s.csv\n" % (_period))            
        
            fRVI.close()
        
            # run ReadVarESO
            jobReadVarESO = subprocess.Popen(os.path.join(readvarsesoLocation, "ReadVarsESO%s" % (exeExtension)) + (" customNoMASS_%s.rvi " % (_period)) + _period + " unlimited", shell=True, cwd=simDirectory, stdout=subprocess.PIPE)
            jobReadVarESOOutput = jobReadVarESO.communicate()[0]
            outputEPlusPeriodMessage = jobReadVarESOOutput.decode('unicode_escape')
            periods[_period] = outputEPlusPeriodMessage
        
        processingTime = (time.time() - startTime)
        
        # remove EPlus output files
        remFileExtensions = [".audit", ".bnd", ".edd", ".eio", ".end", ".eso", ".mdd", ".mtd", ".rdd", ".shd", ".sql", ".dbg", ".mtr"]
        additionalFiles = ["readvars.audit", "sqlite.err", "epluszsz.csv"]
        
        if not keepEPlusOutput:           
            # remove eplusoutput files by extension
            for i in remFileExtensions:
                if os.path.exists(os.path.join(simDirectory, "eplusout%s" % (i))):
                    try:
                        os.remove(os.path.join(simDirectory, "eplusout%s" % (i)))
                    except:
                        pass
                    
            # remove files by name
            for i in additionalFiles:
                if os.path.exists(os.path.join(simDirectory, i)):
                    try:
                        os.remove(os.path.join(simDirectory, i))
                    except:
                        pass
                    
            # remove temp directory
            try:
                shutil.rmtree(os.path.join(simDirectory, "tmp-fmus"))
            except:
                pass
            
        print("================================================")
        print("(%.2f secs)" % (processingTime))
        print(outputEPlusMessage)
        _app.log(outputEPlusMessage)        
        print("- - - - - - - - - - - - - - - - - - - - - - - - ")
        for _key, _value in periods.items():
            print(_key, ": ", _value)
        
        return typeOfSimulation, simId, outputEPlusMessage, periods, processingTime
        # +--------
        
        
    def saveAndRun(self):
        if self._parentWidget.appState() != typeOfAppStatus.IDLE:
            messagebox.showerror(title='Error!', message="The application is busy")
            return

        #  lock the app
        _app = self._parentWidget
        _app.appState(typeOfAppStatus.WRITING)

        # 1. Validate data
        # 1.1 verify output files and directories
        _outputFilesExist = self.outputFileDirectoryExist()
        if _outputFilesExist[0] == False:
            _app.appState(typeOfAppStatus.IDLE)
            messagebox.showerror(title='Error!', message="%s not found!" % (_outputFilesExist[1]))
            return

        # 1.2 verify the list of zones in the idf file and configuration
        pZonesIDF = self.getZoneLisFromIDF().keys()
        pZonesGUI = self._parentWidget.getListOfItemsByType(typeOfClass.BUILDING_ZONE)
        _pZonesGUI = []
        
        # ACTIVE zones only!!!
        _pZonesGUIWithWindows = []

        if len(pZonesIDF) == 0:
            _app.appState(typeOfAppStatus.IDLE)
            messagebox.showerror(title='Error!', message="No zones found in the IDF file")
            return

        if pZonesGUI is None or len(pZonesGUI) == 0:
            _app.appState(typeOfAppStatus.IDLE)
            messagebox.showerror(title='Error!', message="No zones found in the configuration")
            return

        # create array with zone names only
        for i in pZonesGUI:
            _pZonesGUI.append(i.name)
            if i.windowCount > 0:
                _pZonesGUIWithWindows.append(i.name)

        # compare list of zones
        zonesComp = self.compareLists(pZonesIDF, _pZonesGUI)
        if not zonesComp[0]:
            dlgConfirmZones = FrmListOfZonesVerification(self._parentWidget.master, pZonesIDF, _pZonesGUI)

            self._parentWidget.master.wait_window(dlgConfirmZones.top)
            if dlgConfirmZones.error:
                _app.appState(typeOfAppStatus.IDLE)
                messagebox.showerror(title='Error!', message=dlgConfirmZones.message)
                return

            if not dlgConfirmZones.confirm:
                _app.appState(typeOfAppStatus.IDLE)
                return

        # 1.3 verify building, zones, agents, NoMASS models and write the SimulationConfig.xml file
        filename = self._parentWidget.saveProject()
        if filename is None:
            _app.appState(typeOfAppStatus.IDLE)
            return

        # switch to the log screen
        _app.nbMain.select(_app.tabLog)
        #_app.update()
        _app.refreshGUI()
        
        sessionID = str(uuid.uuid4())
        sessionPath = os.path.join(self.outputDirectory, sessionID)
        simFolders = ("Static", "Random")
        startTimeStamp = datetime.datetime.now()
        _app.log("")
        _app.log("")
        _app.log(" Output configuration file: %s" % (filename))
        _app.log("")
        _app.log("============================================================")
        _app.log(" Running replicates")
        _app.log(" Start time: %s" % (str(startTimeStamp)))
        _app.log(" Session ID: %s" % (sessionID))
        _app.log("")
        
        # 2. Generate output folders (Static, Random)
        try:
            _app.log(" creating output directories...")
            if not os.path.exists(sessionPath):
                os.makedirs(sessionPath)

            for _sim in simFolders:
                os.makedirs(os.path.join(sessionPath, _sim))
                _app.log("    - %s" % (_sim))
            _app.log("")
        except:
            _app.appState(typeOfAppStatus.IDLE)
            messagebox.showerror(title='Error!', message="Error while creating output directories")
            return

        _app.log(" preparing simulation folders")
        _app.log(" - copy SimulationConfig.xml to the root folder")
        copyfile(filename, os.path.join(sessionPath, "SimulationConfig.xml"))
        _app.log(" - copy X.idf to the root folder")
        copyfile(self.idfFilename, os.path.join(sessionPath, Utils.IO.baseFilename(self.idfFilename)))
        # add IDF addenda to execute co-simulation
        #print("------------------------", self._attachDayCtrl.get(), "---")
        self.appendIDFAddenda(os.path.join(sessionPath, Utils.IO.baseFilename(self.idfFilename)), _pZonesGUIWithWindows, _app.simulation.eplusVersion, self._attachDayCtrl.get(), self._attachWinState0.get())

        modelDescriptionFilename = os.path.join(sessionPath, "modelDescription.xml")
        modelDescriptionXML = self.createModelDescription(_pZonesGUIWithWindows, _app.simulation.eplusVersion)
        modelDescriptionXML.write(modelDescriptionFilename)
        _app.log(" - random Seed and static Window, Shade devices (%s)" % (str(_app.simulation.numberOfReplicates)))


        # modified on 24.06.2019
        periods = {}
        if self._storeRunperiod.get():
            periods['RunPeriod'] = ""
        if self._storeMonthly.get():
            periods['Monthly'] = ""
        if self._storeTimestep.get():
            periods['TimeStep'] = ""

        # +--- create batch file
        epVersion = _app.simulation.eplusVersion.replace(".","")
        weatherFilename = Utils.IO.baseFilename(self.weatherFilename)
        batchExtension = ""
        pauseCommand = "pause"
        clearCommand = "clear"
        exeExtension = ""
        if Utils.IO.isWindows():
            batchExtension = "bat"
            pauseCommand  = "pause"
            exeExtension = ".exe"
            clearCommand = "cls"
        if Utils.IO.isLinux():
            batchExtension = "sh"
            pauseCommand  = "pause"
            clearCommand = "clear"
        batchFilename = os.path.join(sessionPath, "eplus_%s_%s.%s" % (Utils.IO.baseFilename(self.idfFilename), epVersion, batchExtension))
        fBatch = open(batchFilename,'w')
        fBatch.write("@echo OFF\n")
        fBatch.write("%s\n" % (clearCommand))
        fBatch.write("set idffilename=%~n0\n")
        fBatch.write("set idffilename=%idffilename:~6,-3%\n")
        fBatch.write("echo \"+-----------------\"\n")
        fBatch.write("echo Processing IDF filename: \"%idffilename%\"\n")
        fBatch.write("%s -w %s %%idffilename%%\n" % (os.path.join(self.eplusLocation, "energyplus%s" % (exeExtension)), weatherFilename))
        fBatch.write("%s\n" % (pauseCommand))
        fBatch.close()
        
        batchVarFilename = os.path.join(sessionPath, "eplus_%s_%s_var.%s" % (Utils.IO.baseFilename(self.idfFilename), epVersion, batchExtension))
        fBatchVar = open(batchVarFilename,'w')
        fBatchVar.write("@echo OFF\n")
        fBatchVar.write("%s\n" % (clearCommand))
        fBatchVar.write("echo \"+-----------------\"\n")
        
        for _period in periods:
            fBatchVar.write("echo .\n")
            fBatchVar.write("echo ...\n")
            fBatchVar.write("echo Processing ReadVarsESO %s \n" % (_period))
            fBatchVar.write("%s \n" % (os.path.join(os.path.dirname(self.eplusLocation), "ReadVarsESO%s" % (exeExtension)) + (" customNoMASS_%s.rvi " % (_period)) + _period + " unlimited"))
            fBatchVar.write("echo \n\n")
        fBatchVar.write("echo \"+-----------------\"\n")
        fBatchVar.write("%s\n" % (pauseCommand))
        fBatchVar.close()
        # +--- create batch file

        # verify the seed value
        if _app.simulation.seed <= 0:
            random.seed()
        else:
            random.seed(_app.simulation.seed)

        # create folder and copy .epw, .idf, .xml and .fmu files
        for i in range(_app.simulation.numberOfReplicates):
            dest = os.path.join(sessionPath, os.path.join(simFolders[0], "Simulation_%s" % (str(i+1))))
            os.makedirs(dest)
            _insSimConfig = Simulation(_app.simulation)

            _insSimConfig.seed = random.randint(1, 99999)
            _insSimConfig.randomWindow = 0
            _insSimConfig.randomShade = 0
            _insSimConfig.attachDayCtrl = self._attachDayCtrl.get()
            _insSimConfig.attachWinState0 = self._attachWinState0.get()
            _insSimConfig.filename = os.path.join(dest, "SimulationConfig.xml")
            _insSimConfig.saveXML()
            self.copyFilesToSimulationFolder(sessionPath, dest, filename, modelDescriptionFilename, batchFilename)
            self.copyFilesToSimulationFolder(sessionPath, dest, filename, modelDescriptionFilename, batchVarFilename)


        _app.log(" - random Seed, Window and Shade devices (%s)" % (str(_app.simulation.numberOfReplicatesRandom)))

        pWindows = self._parentWidget.getListOfItemsByType(typeOfClass.MODEL_WINDOW)
        pShades = self._parentWidget.getListOfItemsByType(typeOfClass.MODEL_SHADE)

        # create folder and copy .epw, .idf, .xml and .fmu files
        for i in range(_app.simulation.numberOfReplicatesRandom):
            dest = os.path.join(sessionPath, os.path.join(simFolders[1], "Simulation_%s" % (str(i+1))))
            os.makedirs(dest)
            _insSimConfig = Simulation(_app.simulation)

            _insSimConfig.seed = random.randint(1, 99999)
            _insSimConfig.randomWindow = 1
            _insSimConfig.randomShade = 1
            _insSimConfig.attachDayCtrl = self._attachDayCtrl.get()
            _insSimConfig.attachWinState0 = self._attachWinState0.get()
            _insSimConfig.filename = os.path.join(dest, "SimulationConfig.xml")

            # randomise window and shade
            for agent in _insSimConfig.building.occupants:
                windowId = random.randint(1, len(pWindows))
                windowName = self.getNameFromListById(pWindows, windowId)

                shadeId = random.randint(1, len(pShades))
                shadeName = self.getNameFromListById(pShades, shadeId)

                agent.windowId = windowId
                agent.window = windowName

                agent.shadeId = shadeId
                agent.shade = shadeName

            _insSimConfig.saveXML()
            print("SimConfig.filename", _insSimConfig.filename)
            #print(_insSimConfig)
            print("+++++++++++")
            self.copyFilesToSimulationFolder(sessionPath, dest, filename, modelDescriptionFilename, batchFilename)
            self.copyFilesToSimulationFolder(sessionPath, dest, filename, modelDescriptionFilename, batchVarFilename)

        # execute simulations in a sequence form. August 2018
        _app.log(" ")
        _app.log(" preparing simulation execution")
        startTime = time.time()
        #_app.log(" start time: %s" % (str(startTime)))
        
        isWindows = Utils.IO.isWindows()        
        eplusSimArgs = []
        for i in range(_app.simulation.numberOfReplicates):
            simDirectory = os.path.join(sessionPath, os.path.join(simFolders[0], "Simulation_%s" % (str(i+1))))
            eplusSimArgs.append((
                    # _app,
                    simFolders[0],
                    i,
                    simDirectory,
                    self.eplusLocation,
                    Utils.IO.baseFilename(self.idfFilename),
                    Utils.IO.baseFilename(self.weatherFilename),
                    # self._allOutputVariables,
                    _app.simulation.outputVariables,
                    self._storeRunperiod.get(),
                    self._storeMonthly.get(),
                    self._storeTimestep.get(),
                    self._keepEPlusOutput.get(),
                    isWindows
            ))
            
        for i in range(_app.simulation.numberOfReplicatesRandom):
            simDirectory = os.path.join(sessionPath, os.path.join(simFolders[1], "Simulation_%s" % (str(i+1))))
            eplusSimArgs.append((
                    # _app,
                    simFolders[1],
                    i,
                    simDirectory,
                    self.eplusLocation,
                    Utils.IO.baseFilename(self.idfFilename),
                    Utils.IO.baseFilename(self.weatherFilename),
                    # self._allOutputVariables,
                    _app.simulation.outputVariables,
                    self._storeRunperiod.get(),
                    self._storeMonthly.get(),
                    self._storeTimestep.get(),
                    self._keepEPlusOutput.get(),
                    isWindows
            ))
        
        uSimIndex = 1
        for _args in eplusSimArgs:
            _app.log("")
            _app.log("")
            _app.log("")
            _app.log("+--------------------")
            _app.log("Simulation (%s) " % str(uSimIndex))
            self.execEPlusSimulationSequential(_args)
            _app.log("+--------------------")
            uSimIndex += 1
            
        _app.log("Finish!")
        _app.log("")
        _app.log("Simulation output folder: %s" % (sessionID))
        _app.log("")
        
        _app.appState(typeOfAppStatus.IDLE)
        messagebox.showinfo(title='NoMASS', message="Simulation has been completed\nFind output at folder %s" % (sessionID))
        return

    def __init__(self, master, parent, objSimulation):
        # tk.Frame.__init__(self, master.master)
        form_margin_top = 10
        column_width = 15
        padding_outer = 100
        padding_inner = 3
        padding_top = 1
        padding_btm = 2

        self._parentWidget = master
        self._parentTab = parent

        self._uuid = str(uuid.uuid4())
        # self._typeOfForm = typeOfForm.N_A
        self._frame = tk.Frame(parent, width=parent.winfo_reqwidth(), height=parent.winfo_reqheight())
        self._frame.pack(fill="both")

        self._idfFilename = tk.StringVar()
        self._weatherFilename = tk.StringVar()
        self._outputDirectory = tk.StringVar()
        self._eplusLocation = tk.StringVar()
        self._randomWindow = tk.BooleanVar()
        self._randomShade = tk.BooleanVar()
        self._attachDayCtrl = tk.BooleanVar()
        self._attachWinState0 = tk.BooleanVar()

        self._storeRunperiod = tk.BooleanVar()
        self._storeMonthly = tk.BooleanVar()
        self._storeTimestep = tk.BooleanVar()
        self._keepEPlusOutput = tk.BooleanVar()

        self._allOutputVariables = {}
        self._zoneVariables = Utils.Config.getCatalog("zoneVariables")
        self._environmentVariables = Utils.Config.getCatalog("environmentVariables")
        self._simulationVariables = Utils.Config.getCatalog("simulationVariables")
        self._allOutputVariables = Utils.Functions.concatenateDict(Utils.Functions.concatenateDict(self._zoneVariables, self._environmentVariables), self._simulationVariables)

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="IDF file:", width=column_width, anchor='w')
        lbl.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtIDFFilename = tk.Entry(containerTemp, textvariable=self._idfFilename)
        self.txtIDFFilename.pack(fill='x', expand=True, side="left", padx=(padding_inner, 0))
        self.btnSelectIDFFile = Utils.UI.Controls.ImageButton(containerTemp, Utils.Resources.Icons.folder_open_o_16_0_333333, self.selectIDFFile, "Select file .idf file")
        self.btnSelectIDFFile.pack(side="right", padx=(0, padding_inner))
        containerTemp.pack(fill='x', pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="Weather file:", width=column_width, anchor='w')
        lbl.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtWeatherFilename = tk.Entry(containerTemp, textvariable=self._weatherFilename)
        self.txtWeatherFilename.pack(fill='x', expand=True, side="left", padx=(padding_inner, 0))
        self.btnSelectWeatherFile = Utils.UI.Controls.ImageButton(containerTemp, Utils.Resources.Icons.folder_open_o_16_0_333333, self.selectWeatherFile, "Select file .epw file")
        self.btnSelectWeatherFile.pack(side="right", padx=(0, padding_inner))
        containerTemp.pack(fill='x', pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="Output directory:", width=column_width, anchor='w')
        lbl.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtOutputDirectory = tk.Entry(containerTemp, textvariable=self._outputDirectory)
        self.txtOutputDirectory.pack(fill='x', expand=True, side="left", padx=(padding_inner, 0))
        self.btnSelectOutputDirectory = Utils.UI.Controls.ImageButton(containerTemp, Utils.Resources.Icons.folder_open_o_16_0_333333, self.selectOutputDirectory, "Select output directory")
        self.btnSelectOutputDirectory.pack(side="right", padx=(0, padding_inner))
        containerTemp.pack(fill='x', pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="EPlus location:", width=column_width, anchor='w')
        lbl.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtEPlusLocation = tk.Entry(containerTemp, textvariable=self._eplusLocation)
        self.txtEPlusLocation.pack(fill='x', expand=True, side="left", padx=(padding_inner, 0))
        self.btnSelectEPlusLocation = Utils.UI.Controls.ImageButton(containerTemp, Utils.Resources.Icons.folder_open_o_16_0_333333, self.selectEPlusLocation, "Select EnergyPlus app folder")
        self.btnSelectEPlusLocation.pack(side="right", padx=(0, padding_inner))
        containerTemp.pack(fill='x', pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="Randomise devices", width=int(column_width*1.25), anchor='w')
        lbl.pack(side="left", padx=(2*padding_inner, padding_inner))
        chk = tk.Checkbutton(containerTemp, text="Windows", anchor='w', onvalue=1, offvalue=0, variable=self._randomWindow, state="disabled")
        chk.pack(side="left", padx=(padding_inner, 0))
        chk = tk.Checkbutton(containerTemp, text="Shades", anchor='w', onvalue=1, offvalue=0, variable=self._randomShade, state="disabled")
        chk.pack(side="left", padx=(padding_inner, 0))
        containerTemp.pack(fill='x', pady=(form_margin_top, 0))
        
        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="Attach '_DaylCtrl' to Daylighting Reference Point", width=int(column_width*2.5), anchor='w')
        lbl.pack(side="left", padx=(2*padding_inner, padding_inner))
        chk = tk.Checkbutton(containerTemp, text="", anchor='w', onvalue=1, offvalue=0, variable=self._attachDayCtrl)
        chk.pack(side="left", padx=(padding_inner, 0))
        containerTemp.pack(fill='x', pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="Attach '0' to Zone WindowState (ZoneWindowState0)", width=int(column_width*2.75), anchor='w')
        lbl.pack(side="left", padx=(2*padding_inner, padding_inner))
        chk = tk.Checkbutton(containerTemp, text="", anchor='w', onvalue=1, offvalue=0, variable=self._attachWinState0)
        chk.pack(side="left", padx=(padding_inner, 0))
        containerTemp.pack(fill='x', pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="Data to store", width=int(column_width*1.25), anchor='w')
        lbl.pack(side="left", padx=(2*padding_inner, padding_inner))
        chk = tk.Checkbutton(containerTemp, text="Runperiod", anchor='w', onvalue=True, offvalue=False, variable=self._storeRunperiod)
        chk.pack(side="left", padx=(padding_inner, 0))
        chk = tk.Checkbutton(containerTemp, text="Monthly", anchor='w', onvalue=True, offvalue=False, variable=self._storeMonthly)
        chk.pack(side="left", padx=(padding_inner, 0))
        chk = tk.Checkbutton(containerTemp, text="Timestep", anchor='w', onvalue=True, offvalue=False, variable=self._storeTimestep)
        chk.pack(side="left", padx=(padding_inner, 0))
        containerTemp.pack(fill='x', pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="Keep EPlus output files?", width=int(column_width*1.25), anchor='w')
        lbl.pack(side="left", padx=(2*padding_inner, padding_inner))
        chk = tk.Checkbutton(containerTemp, text="", anchor='w', onvalue=True, offvalue=False, variable=self._keepEPlusOutput, state="normal")
        chk.pack(side="left", padx=(padding_inner, 0))
        containerTemp.pack(fill='x', pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.btnSaveAndRun = tk.Button(containerTemp, text="Save and Run Simulations", anchor="c", width=20, command=self.saveAndRun)
        self.btnSaveAndRun.pack(expand=True, padx=(padding_inner, padding_inner))
        containerTemp.pack(fill='x', pady=(form_margin_top, 0))

        self._idfFilename.set(objSimulation.idfFilename)
        self._weatherFilename.set(objSimulation.weatherFilename)
        self._outputDirectory.set(objSimulation.outputDirectory)
        self._eplusLocation.set(objSimulation.eplusLocation)
        self._randomWindow.set(objSimulation.randomWindow)
        self._randomShade.set(objSimulation.randomShade)
        self._attachDayCtrl.set(objSimulation.attachDayCtrl)
        self._attachWinState0.set(objSimulation.attachWinState0)
        
        self._storeRunperiod.set(True)
        self._storeMonthly.set(True)
        self._storeTimestep.set(False)
        return
# end of FrmRun