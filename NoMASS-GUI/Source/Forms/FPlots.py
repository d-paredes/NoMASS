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

class FrmPlots(object):
    @property
    def ID(self):
        return self._uuid

    @property
    def Frame(self):
        return self._frame

    def selectOutputDirectory(self):
        currentPath = self._szOutputDirectory.get()
        if not os.path.exists(currentPath):
            self._szOutputDirectory.set(Utils.Config.getAppLocation())
            currentPath = self._szOutputDirectory.get()

        folder = filedialog.askdirectory(title="Select simulation output directory", initialdir=currentPath, mustexist=True)
        if folder:
            try:
                self._szOutputDirectory.set(folder)
            except:
                raise Exception("Error while selecting output directory")
                return
            
            self.loadSimulation()
        return
    # end of selectOutputDirectory

    def loadSimulationsAndPlot(self):
        updateProgressBar(0)
        for i in range(100):
            updateProgressBar(i)
        self._app.log("Simulation file has been loaded!")
        self._app.sbmessage("Simulation file has been loaded!")
        return

    def loadAreaPerZone(self):
        idfFilename = os.path.join(self._outputDirectory, Utils.IO.baseFilename(self.simulation.idfFilename))
        f = open(idfFilename, "r")
        fstream = f.read()
        pZoneTags = re.findall(r"[.]*Zone[,][^;]*[;]+", fstream)
        for _tag in pZoneTags:
            pZonesSelection = re.findall(r"^Zone[,][^,]*[,]+", _tag)
            for _zoneIDF in pZonesSelection:
                _zoneID = _zoneIDF[5 : len(_zoneIDF)-1]
                _zoneID = _zoneID.strip()
                for _zone in self.simulation.building.zones:
                    if _zoneID.lower() == _zone.name.lower():
                        pFloorAreaSelection = re.findall(r".*Floor Area.*", _tag)
                        if pFloorAreaSelection is not None and len(pFloorAreaSelection) == 1:
                            pNumberSelection = re.findall(r"^[^,]*", pFloorAreaSelection[0].strip())
                            _zone.area = float(pNumberSelection[0].strip())
        return

    def loadSimulation(self):
        if len(self._szOutputDirectory.get().strip()) == 0:
            messagebox.showerror(title='Error!', message="Select a valid folder containing the SimulationConfig.xml file")
            return

        self._outputDirectory = self._szOutputDirectory.get().strip()
        
        simulationFilename = os.path.join(self._outputDirectory, "SimulationConfig.xml")

        if not os.path.exists(simulationFilename):
            messagebox.showerror(title='Error!', message="Select a valid folder containing the SimulationConfig.xml file")
            return

        self.simulation = Simulation()
        self.simulation.loadFromFile(simulationFilename)
        
        self._app.log("Simulation file has been loaded!")
        self._app.sbmessage("Simulation file has been loaded!")
        self._app.refreshGUI();
        return


    def exportVariable(self):
        pass

    def getVariableName(self, variableName, periodType):
        for insVariable in self.simulation.outputVariables:
            rExpression = "%s.*[]+[\(]+%s[\)]+$" % (insVariable.strip(), periodType.strip())
            pOccurences = re.findall(rExpression, variableName.strip())

            if(len(pOccurences) == 1):
                # return insVariable
                return pOccurences[0]
        return None, None

    def convertJulesToWMS(self, value, area):
      return (value * 0.0000002778) / area

    def generateGraph(self, ppData, xTickLabels, graphSettings, xLabelRotation, padding_btm, legendText=None, szFigFilename="image.png"):
        title_fontsize = 9
        axis_fontsize = 8
        tick_fontsize = 6
        legend_fontsize = 7
        # prepare
        fig = Figure(figsize=(5,5))
        a = fig.add_subplot(111)
        bplot = a.boxplot(ppData, 0, '')
        
        # format
        a.set_ylabel(graphSettings["ylabel"], fontsize=axis_fontsize)
        a.set_xlabel(graphSettings["xlabel"], fontsize=axis_fontsize)
        a.set_title(graphSettings["title"], fontsize=title_fontsize)
        
        if graphSettings["ymin"] != None and graphSettings["ymax"] != None:
            a.set_ylim(bottom=graphSettings["ymin"], top=graphSettings["ymax"])
        
        if xLabelRotation != 0:
            a.set_xticklabels(xTickLabels, fontsize=tick_fontsize, rotation=xLabelRotation, ha='right', va='center', wrap=True)
        else:
            a.set_xticklabels(xTickLabels, fontsize=tick_fontsize, rotation=xLabelRotation, ha='center', va='center', wrap=True)
        
        if legendText is not None:
            a.legend([bplot['boxes'][0]], [legendText], loc='upper right', framealpha=.3, frameon=False, labelspacing=1, fontsize=legend_fontsize, handlelength=0)
        
        for label in a.get_yticklabels():
            label.set_fontsize(tick_fontsize)
            
        a.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

        for box in bplot['boxes']:
            box.set(color='#000000', linewidth=1)

        for whisker in bplot['whiskers']:
            whisker.set(color='#000000', linewidth=1, linestyle='--')

        for cap in bplot['caps']:
            cap.set(color='#000000', linewidth=1)

        for median in bplot['medians']:
            median.set(color='#ff0000', linewidth=1)

        for flier in bplot['fliers']:
            flier.set(marker='o', color='#0000ff', alpha=0.5, linestyle='none')
        
        # adjust bottom room
        fig.subplots_adjust(bottom=padding_btm)
        containerTemp = tk.Frame(self.plotCanvas)
        containerTemp.pack_propagate(False)
        containerTemp.config(width=400, height=400)
        containerTemp.config(background='#ffffff')
        canvas = FigureCanvasTk(fig, master=containerTemp)
        canvas.figure.subplots_adjust(bottom=padding_btm)
        try:
            canvas.show()
        except:
            try:
                canvas.draw()
            except:
                print("canvas.show()...canvas.draw()...error")
        
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        containerTemp.pack(fill=tk.X, pady=(0,0))
        
        # write as image
        fig.savefig(szFigFilename, type="png", dpi=300)
        return
    # end of generateGraph

    def getVarColumnIndex(self, header, varName):
        for i in range(len(header)):
            if header[i].lower() == varName.lower():
                return i
        return -1
    
    def generateHeader(self, periodType, varNameLabels):
        pMonthLabelNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        output = []
        if periodType.lower() == "runperiod":
            output.append("Replicate")
            output.append("Date/Time")
            for varName in sorted(varNameLabels):
                output.append(varName)
        elif periodType.lower() == "monthly":
            output.append("Replicate")
            for uMonth in range(12):
                output.append(pMonthLabelNames[uMonth])
        else:
            messagebox.showerror(title='Error!', message="ERROR -999")
            return []
        
        return output
    # end of generateHeader
    
            
    def collectDataEPlus(self, rootFolder, parentFolder, periodType, noReplicates, pVariableZoneColumn):
        ppData = []
        pHeader = self.generateHeader(periodType, sorted(pVariableZoneColumn.keys()))
        # + runperiod
        # | Replicate | Date-Time | Variable Name
        # +------------------------------------
        # | mothly
        # | Replicate | Month -> Jan | Feb | ... | Dec
        for uReplicate in range(noReplicates):
            # set filename
            csvFilename = os.path.join(rootFolder, os.path.join(parentFolder, os.path.join("Simulation_%s" % str(uReplicate+1), "eplusout_%s.csv" % (periodType))))
            # check file exists
            if not os.path.exists(csvFilename):
                messagebox.showerror(title='Error!', message="File %s does not exists!" % (csvFilename))
                return [], []
            
            # get data and header
            ds = pd.read_csv(csvFilename)
            header = ds.columns.values.tolist()
            
            # extract Date?Time and data from each column-variable name
            if periodType.lower() == "runperiod":
                dtColumn = ds[["Date/Time"]]
                for uRow in range(len(dtColumn)):
                    newRow = []
                    newRow.append(uReplicate+1)
                    newRow.append(ds.values[uRow][0])
                    # extract row value for column equals to variable name
                    for varName in sorted(pVariableZoneColumn.keys()):
                        uCol = self.getVarColumnIndex(header, pVariableZoneColumn[varName])
                        if uCol == -1:
                            messagebox.showerror(title='Error!', message="ERROR -999")
                            return [], []
                        newRow.append(ds.values[uRow][uCol])
                    
                    # append row to ppData
                    ppData.append(newRow)
                    
            elif periodType.lower() == "monthly":
                dtColumn = ds[["Date/Time"]]
                newRow = []
                newRow.append(uReplicate+1)
                for uRow in range(len(dtColumn)):
                    for varName in sorted(pVariableZoneColumn.keys()):
                        uCol = self.getVarColumnIndex(header, pVariableZoneColumn[varName])
                        if uCol == -1:
                            messagebox.showerror(title='Error!', message="ERROR -999")
                            return [], []
                        newRow.append(ds.values[uRow][uCol])
                ppData.append(newRow)
                
        return ppData, pHeader
    
    
    def collectDataNoMASS(self, rootFolder, parentFolder, noReplicates, timeStepsHour, pVariableZoneColumn):
        if len(pVariableZoneColumn) != 1:
            return [], []
        
        ppData = []
        pHeader = self.generateHeader("Monthly", sorted(pVariableZoneColumn.keys()))
        
        pVariableColIndex = {}
        
        pDayMonthIndex = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        # + runperiod
        # | Replicate | Date-Time | Variable Name
        # +------------------------------------
        # | mothly
        # | Replicate | Month -> Jan | Feb | ... | Dec
        for uReplicate in range(noReplicates):
            csvFilename = os.path.join(rootFolder, os.path.join(parentFolder, os.path.join("Simulation_%s" % str(uReplicate+1), "NoMASS.csv")))
            if not os.path.exists(csvFilename):
                print("File %s does not exists!" % (csvFilename))
                messagebox.showerror(title='Error!', message="File %s does not exists!" % (csvFilename))
                return
            
            # get data and header
            ds = pd.read_csv(csvFilename)
            header = ds.columns.values.tolist()
                    
            newRow = []
            newRow.append(uReplicate+1)
            
            # divide data into chunks, monthly
            uSum = 0
            uLower = 0
            uUpper = 0
            for uMonth in range(len(pDayMonthIndex)):
                if uMonth == 0:
                    uLower = 0;
                    uUpper = pDayMonthIndex[uMonth] * 24 * timeStepsHour
                else:
                    uLower = uSum
                    uUpper = uLower + (pDayMonthIndex[uMonth] * 24 * timeStepsHour)
                
                ds_month = ds.iloc[uLower:uUpper]
                
                # process data
                # length of pVariableZoneColumn equals to 1
                dSum = 0.0
                for _var in sorted(pVariableZoneColumn.keys()):
                    dSum = ds_month[pVariableZoneColumn[_var]].sum()                   
                    newRow.append(dSum)
                
                # update month index
                uSum += pDayMonthIndex[uMonth] * 24 * timeStepsHour
                
            ppData.append(newRow)

        return ppData, pHeader

    def writeData(self, ppData, pHeader, szFilename):
        csvfile = pd.DataFrame(data=ppData, columns=pHeader)
        csvfile.to_csv(szFilename, index=False)
        return True
    # end of writeData
    
    def preProcessData(self, ppData, pHeader, pZones):
        # convert units from J to KWh/m^2
        for uRow in range(len(ppData)):
            # this nested for loop can be improved by turning ucol, urow
            for _zone in pZones:
                uCol = self.getVarColumnIndex(pHeader, _zone.name)
                dZoneFloorArea = _zone.floorArea
                dValue = ppData[uRow][uCol]
                ppData[uRow][uCol] = self.convertJulesToWMS(ppData[uRow][uCol], dZoneFloorArea)
        return ppData
    # end of preProcessData

    def preProcessDataPerZone(self, ppData, dZoneFloorArea, uLeftColumn=0):
        # convert units from J to KWh/m^2
        for uRow in range(len(ppData)):
            for uCol in range(uLeftColumn, len(ppData[0])):
                ppData[uRow][uCol] = self.convertJulesToWMS(ppData[uRow][uCol], dZoneFloorArea)
        return ppData
    # end of preProcessDataPerZone
    
    def generateGraphs(self, rootFolder, parentFolder, noReplicates, periodType, varName, timeStepsHour):
        self._app.log("")
        self._app.log("--------------------------------------------------")
        self._app.log("Plotting from %s (%s)" % (parentFolder, periodType))
        self._app.log("  Replicates: %s" % (str(noReplicates)))
        self._app.log("  Variable: %s" % (varName))
        self._app.log("Collecting data...")
        
        # collect data from cvs file based on variable name. Some comes from eplusout.csv and others from NoMASS.csv
        energyUnit = "J"
        eplusVarName = str(self._variableOptions[varName]["eplusVarName"]).replace("__UNIT__", energyUnit).replace("__PERIOD__", periodType)
        dataFileName = str(self._variableOptions[varName]["filename"]).replace("__PERIOD__", periodType)
        outputFilename = str(self._variableOptions[varName]["outFilename"]).replace("__UNIT__", energyUnit).replace("__PERIOD__", periodType).replace("__ZONE__","").replace(" ","_").replace(":","_")
        varUnit = str(self._variableOptions[varName]["unit"])
        
        ppData = []
        pHeader = []
        
        pVariableZoneColumn = {}
        pZones = [] #list of zones to plot
        
        # clean canvas
        for imgPlot in self.plotCanvas.winfo_children():
            imgPlot.destroy()
        self.containerPlot.updateViewPort()
        
        if dataFileName == "NoMASS.csv":
        # NoMASS variables
            xTickLabels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            plotSettings_ = self._variableOptions[varName]["plotSettings"]
            plotSettings_["xlabel"] = plotSettings_["xlabel-monthly"]
            plotSettings_["ymin"] = 0
            plotSettings_["ymax"] = 1
                                
            # create list of zones
            for _zone in self.simulation.building.zones:
                if varName.lower() == "windowstate0" or \
                   varName.lower() == "blindfraction":
                    if _zone.windowCount > 0:
                        pZones.append(_zone)
                else:
                    pZones.append(_zone)
                    
            for _zone in pZones:
                pVariableZoneColumn.clear()
                pVariableZoneColumn[_zone.name] = eplusVarName.replace("__ZONE__", _zone.name)
                            
                szFilename = os.path.join(rootFolder, os.path.join(parentFolder, "%s_%s_%s.csv" % (_zone.name.replace(" ","_").replace(":","_"), outputFilename, parentFolder.lower())))
                if not os.path.exists(szFilename):
                    ppData, pHeader = self.collectDataNoMASS(rootFolder, parentFolder, noReplicates, timeStepsHour, pVariableZoneColumn)
                    self.writeData(ppData, pHeader, szFilename)   
                else:
                    _dataFrame = pd.read_csv(szFilename)
                    
                    ppData = _dataFrame.values
                    pHeader = _dataFrame.columns.values.tolist()
                
                # prepare data, normalise data using the total possible 
                pDayMonthIndex = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                
                for uRow in range(noReplicates):
                    for uMonth in range(len(pDayMonthIndex)):
                        ppData[uRow][uMonth+1] = float(ppData[uRow][uMonth+1]) / float(pDayMonthIndex[uMonth] * 24 * timeStepsHour)
                
                # write data into disc
                szFilename = os.path.join(rootFolder, os.path.join(parentFolder, "%s_%s[Norm]_%s.csv" % (_zone.name.replace(" ","_").replace(":","_"), outputFilename, parentFolder.lower())))
                self.writeData(ppData, pHeader, szFilename)   
                                
                # do plot
                # prepare data
                leftColumn = 1                      # skip "Replicate and Date/Time" columns
                # convert ppData into array of "double" values only!
                dataFrame = pd.DataFrame(data=ppData, columns=pHeader)
                ppData_ = dataFrame.values
                pHeader_ = dataFrame.columns.values.tolist()
                
                ppData_ = ppData_[:,leftColumn:]
                pHeader_ = pHeader_[leftColumn:]
                
                self.generateGraph(ppData_, 
                                   xTickLabels, 
                                   plotSettings_,
                                   0,
                                   0.1,
                                   _zone.name,
                                   os.path.join(rootFolder, os.path.join(parentFolder, "%s_%s[Norm]_%s.png" % (_zone.name.replace(" ","_").replace(":","_"), outputFilename.replace("[J]", "[W]"), parentFolder.lower()))))
                self.containerPlot.updateViewPort()
                
                # REFRESH
                ##self.parent.update()
                self._app.sbmessage("Generating graph...")
                self._app.refreshGUI()
                
        else:
        # EnergyPlus variables
            # +-------- create list of zones, only those with windows
            for _zone in self.simulation.building.zones:
                pZones.append(_zone)
            # +-------------------------------------------------------                    
                    
            if periodType.lower() == "runperiod":
            # EnergyPlus variables, RunPeriod
                for _zone in pZones:
                    pVariableZoneColumn[_zone.name] = eplusVarName.replace("__ZONE__", _zone.name)
                                
                szFilename = os.path.join(rootFolder, os.path.join(parentFolder, "%s_%s.csv" % (outputFilename, parentFolder.lower())))
                if not os.path.exists(szFilename):
                    ppData, pHeader = self.collectDataEPlus(rootFolder, parentFolder, periodType, noReplicates, pVariableZoneColumn)
                    self.writeData(ppData, pHeader, szFilename)   
                else:
                    _dataFrame = pd.read_csv(szFilename)
                    
                    ppData = _dataFrame.values
                    pHeader = _dataFrame.columns.values.tolist()
                                
                if varUnit.upper() == "J":
                    ppData = self.preProcessData(ppData, pHeader, pZones)
                # write data into disc
                szFilename = os.path.join(rootFolder, os.path.join(parentFolder, "%s_%s.csv" % (outputFilename.replace("[J]", "[W]"), parentFolder.lower())))
                self.writeData(ppData, pHeader, szFilename)
                
                # +------------------ do Plot                
                # prepare data
                leftColumn = 2                      # skip "Replicate and Date/Time" columns
                # convert ppData into array of "double" values only!
                dataFrame = pd.DataFrame(data=ppData, columns=pHeader)
                ppData_ = dataFrame.values
                pHeader_ = dataFrame.columns.values.tolist()
                
                ppData_ = ppData_[:,leftColumn:]
                pHeader_ = pHeader_[leftColumn:]
                
                plotSettings_ = self._variableOptions[varName]["plotSettings"]
                plotSettings_["xlabel"] = plotSettings_["xlabel-runperiod"]
                plotSettings_["ymin"] = None
                plotSettings_["ymax"] = None
                self.generateGraph(ppData_, 
                                   pHeader_, 
                                   plotSettings_, 
                                   90, 
                                   0.3,
                                   None,
                                   os.path.join(rootFolder, os.path.join(parentFolder, "%s_%s.png" % (outputFilename.replace("[J]", "[W]"), parentFolder.lower()))))
                self.containerPlot.updateViewPort()
                
                # REFRESH
                self._app.sbmessage("Generating graph...")
                self._app.refreshGUI()
            # EnergyPlus variables, Monthly
            elif periodType.lower() == "monthly":               
            # EnergyPlus variables, Monthly
                xTickLabels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                plotSettings_ = self._variableOptions[varName]["plotSettings"]
                plotSettings_["xlabel"] = plotSettings_["xlabel-monthly"]
                plotSettings_["ymin"] = None
                plotSettings_["ymax"] = None
                
                # prepare data
                leftColumn = 1                      # skip "Replicate and Date/Time" columns
                
                for _zone in pZones:
                    pVariableZoneColumn.clear()
                    pVariableZoneColumn[_zone.name] = eplusVarName.replace("__ZONE__", _zone.name)
                    
                    szFilename = os.path.join(rootFolder, os.path.join(parentFolder, "%s_%s_%s.csv" % (_zone.name.replace(" ","_").replace(":","_"), outputFilename, parentFolder.lower())))
                    if not os.path.exists(szFilename):
                        ppData, pHeader = self.collectDataEPlus(rootFolder, parentFolder, periodType, noReplicates, pVariableZoneColumn)
                        self.writeData(ppData, pHeader, szFilename)   
                    else:
                        _dataFrame = pd.read_csv(szFilename)
                        
                        ppData = _dataFrame.values
                        pHeader = _dataFrame.columns.values.tolist()
                                            
                    if varUnit.upper() == "J":
                        ppData = self.preProcessDataPerZone(ppData, _zone.floorArea, leftColumn)
                                            
                    # write data into disc
                    szFilename = os.path.join(rootFolder, os.path.join(parentFolder, "%s_%s_%s.csv" % (_zone.name.replace(" ","_").replace(":","_"), outputFilename.replace("[J]", "[W]"), parentFolder.lower())))
                    self.writeData(ppData, pHeader, szFilename)   
                    
                    # convert ppData into array of "double" values only!
                    dataFrame = pd.DataFrame(data=ppData, columns=pHeader)
                    ppData_ = dataFrame.values
                    pHeader_ = dataFrame.columns.values.tolist()
                    
                    ppData_ = ppData_[:,leftColumn:]
                    pHeader_ = pHeader_[leftColumn:]
                    
                    self.generateGraph(ppData_, 
                                       xTickLabels, 
                                       plotSettings_,
                                       0,
                                       0.1,
                                       _zone.name,
                                       os.path.join(rootFolder, os.path.join(parentFolder, "%s_%s_%s.png" % (_zone.name.replace(" ","_").replace(":","_"), outputFilename.replace("[J]", "[W]"), parentFolder.lower()))))
                    self.containerPlot.updateViewPort()
                    
                    # REFRESH
                    self._app.sbmessage("Generating graph...")
                    self._app.refreshGUI()
        return
    # end of generateGraphs
    
    def generateAllGraphs(self):
        if not hasattr(self, 'simulation'):
            return 
        
        typeofSimulation = "Random"
        replicates = 0
        if typeofSimulation.lower() == "static":
            replicates = self.simulation.numberOfReplicates
        if typeofSimulation.lower() == "random":
            replicates = self.simulation.numberOfReplicatesRandom

        timeStepsHour = self.simulation.timeStepsPerHour
        
        for _period in self._pPeriod:
            for _var in sorted(self._variableOptions.keys()):
                if (_period.lower() == "runperiod" and _var.lower() != "windowstate0") or \
                   (_period.lower() == "monthly"):
                    self.generateGraphs(self._outputDirectory, "Random", replicates, _period, _var, timeStepsHour)
                    self._app.refreshGUI()
        self._app.sbmessage("All graphs have been generated")
                
        return
    # end of generateAllGraphs        
    
    def tvwOutputVariables_OnDoubleClickItem(self, event=None):       
        if not hasattr(self, 'simulation'):
            return 
        
        node = self.tvwOutputVariables.selection()[0]
        if node is None:
            return

        typeofSimulation = str(self.tvwOutputVariables.item(node)["values"][0])
        periodType = str(self.tvwOutputVariables.item(node)["values"][1])
        varName = str(self.tvwOutputVariables.item(node)["values"][2])

        if len(varName.strip()) == 0:
            # do nothing. It is a parent node
            return

        replicates = 0
        if typeofSimulation.lower() == "static":
            replicates = self.simulation.numberOfReplicates
        if typeofSimulation.lower() == "random":
            replicates = self.simulation.numberOfReplicatesRandom

        timeStepsHour = self.simulation.timeStepsPerHour

        self._parentTab.config(cursor="wait")
        self._parentTab.update()
        self.generateGraphs(self._outputDirectory, typeofSimulation, replicates, periodType, varName, timeStepsHour)
        self._parentTab.config(cursor="")
        
        self._app.log("")
        self._app.sbmessage("")
        self._app.refreshGUI();
        return

    def initVariableOptions(self):
        self.tvwOutputVariables.delete(*self.tvwOutputVariables.get_children())
        self.tvwOutputVariables.clearOnMove()

        for p in self._pPeriod:
            nPeriod = self.tvwOutputVariables.insert("", "end", text=p, values=["Random", p, ""], tags=["normal", p, ""], open=True)
                        
            for k in sorted(self._variableOptions.keys()):
                if (p.lower() == "runperiod" and k.lower() != "windowstate0") or \
                   (p.lower() == "monthly"):               
                    nVar = self.tvwOutputVariables.insert(nPeriod, "end", text=k, values=["Random", p, k], tags=["normal", p, k], open=True)
        return
        # end of initVariableOptions
        
    def __init__(self, master, parent, objSimulation):
        self._pTypeOfSimulation = ["Static", "Random"]
        self._pPeriod = ["RunPeriod", "Monthly"]
        self._variableOptions = {"Cooling": {"filename" : "eplusout___PERIOD__.csv",
                                             "eplusVarName": "__ZONE__:Zone Air System Sensible Cooling Energy [__UNIT__](__PERIOD__)",
                                             "outFilename": "__ZONE__Zone_CoolingEnergy[__UNIT__](__PERIOD__)",
                                             "unit": "J",
                                             "plotSettings": {
                                                     "title": "Zone Air System Sensible Cooling Energy",
                                                     "ylabel": "$kWh/m^2$",
                                                     "xlabel-runperiod": "Zone",
                                                     "xlabel-monthly": "Period",
                                                     }
                                            },
                                 "Heating": {"filename" : "eplusout___PERIOD__.csv",
                                             "eplusVarName": "__ZONE__:Zone Air System Sensible Heating Energy [__UNIT__](__PERIOD__)",
                                             "outFilename": "__ZONE__Zone_HeatingEnergy[__UNIT__](__PERIOD__)",                                             
                                             "unit": "J",
                                             "plotSettings": {
                                                     "title": "Zone Air System Sensible Heating Energy",
                                                     "ylabel": "$kWh/m^2$",
                                                     "xlabel-runperiod": "Zone",
                                                     "xlabel-monthly": "Period",
                                                     }
                                            },
                                 #"Occupants": {"filename" : "NoMASS.csv",
                                 #            "eplusVarName": "__ZONE__NumberOfOccupants",
                                 #            "outFilename": "__ZONE__NumberOfOccupants(__PERIOD__)",
                                 #            "unit": "U",
                                 #            "plotSettings": {
                                 #                    "title": "Number of occupants",
                                 #                    "ylabel": "People",
                                 #                    "xlabel-runperiod": "Zone",
                                 #                    "xlabel-monthly": "Period",
                                 #                    }
                                 #           },
                                 #"BlindFraction": {"filename" : "NoMASS.csv",
                                 #            "eplusVarName": "__ZONE__BlindFraction",
                                 #            "outFilename": "__ZONE__BlindFraction(__PERIOD__)",
                                 #            "unit": "U",
                                 #            "plotSettings": {
                                 #                    "title": "Blind fraction",
                                 #                    "ylabel": "---",
                                 #                    "xlabel-runperiod": "Zone",
                                 #                    "xlabel-monthly": "Period",
                                 #                    }
                                 #           },
                                 "WindowState0": {"filename" : "NoMASS.csv",
                                             "eplusVarName": "__ZONE__WindowState0",
                                             "outFilename": "__ZONE__WindowState0(__PERIOD__)",
                                             "unit": "U",
                                             "plotSettings": {
                                                     "title": "Window openings",
                                                     "ylabel": "Proportion Of Time Open",
                                                     "xlabel-runperiod": "Zone",
                                                     "xlabel-monthly": "Period",
                                                     }
                                            },
                                 #"LightState": {"filename" : "NoMASS.csv",
                                 #            "eplusVarName": "__ZONE__LightState",
                                 #            "outFilename": "__ZONE__LightState(__PERIOD__)",
                                 #            "unit": "U",
                                 #            "plotSettings": {
                                 #                    "title": "Lights state",
                                 #                    "ylabel": "---",
                                 #                    "xlabel-runperiod": "Zone",
                                 #                    "xlabel-monthly": "Period",
                                 #                    }
                                 #           }
                                }
        form_margin_top = 10
        column_width = 15
        padding_outer = 100
        padding_inner = 5
        padding_top = 2
        padding_btm = 2

        self._app = self._parentWidget = master
        self._parentTab = parent

        self._uuid = str(uuid.uuid4())
        self._frame = tk.Frame(parent, width=parent.winfo_reqwidth(), height=parent.winfo_reqheight())
        self._frame.pack(fill="both", expand=True)

        self._szOutputDirectory = tk.StringVar()

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="Sim. directory:", width=10, anchor='w')
        lbl.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtSimulationstDirectory = tk.Entry(containerTemp, textvariable=self._szOutputDirectory)
        self.txtSimulationstDirectory.pack(fill='x', expand=True, side="left", padx=(padding_inner, 0))
        self.btnGenerateGraphs = Utils.UI.Controls.ImageButton(containerTemp, Utils.Resources.Icons.gears_16_0_333333, self.generateAllGraphs, "Generate graphs")
        self.btnGenerateGraphs.pack(side="right", padx=(0, padding_inner))
        self.btnSelectSimulationsputDirectory = Utils.UI.Controls.ImageButton(containerTemp, Utils.Resources.Icons.folder_open_o_16_0_333333, self.selectOutputDirectory, "Select output directory")
        self.btnSelectSimulationsputDirectory.pack(side="right", padx=(0, padding_inner))
        containerTemp.pack(fill='x', pady=(form_margin_top, 0))

        containerBttmLeft = tk.Frame(self._frame)
        self.tvwOutputVariables = Utils.UI.Controls.ScrolledTreeView(containerBttmLeft, show="tree")#, showToolTip=True)
        self.tvwOutputVariables.column("#0",minwidth=500, stretch=True)
        self.tvwOutputVariables.bind("<Double-1>", self.tvwOutputVariables_OnDoubleClickItem)
        self.tvwOutputVariables.pack(side='left', anchor='w', fill='both', expand=True)
        self.tvwOutputVariables.focus()
        containerBttmLeft.place(relx=0.005, y=40, relheight=.9, relwidth=0.3)

        self.containerPlot = Utils.UI.Controls.ScrollableContainer(self._frame)
        self.containerPlot.place(relx=0.315, y=40, relheight=.9, relwidth=0.68)

        self.plotCanvas = tk.Frame(self.containerPlot.innerframe, width=self.containerPlot.innerframe.winfo_reqwidth(), height=self.containerPlot.innerframe.winfo_reqheight())
        self.plotCanvas.pack(fill="both")

        self.initVariableOptions()
        return
# end of FrmPlots