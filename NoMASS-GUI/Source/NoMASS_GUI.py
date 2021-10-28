#! /usr/bin/env python
# ----------------------------------------------------------------------
# External modules

import uuid
import zipfile
import collections
import datetime
import random
import subprocess
from shutil import copyfile
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvasTk
import sys
import os
import pandas as pd
if sys.version_info[0] == 3:
    import tkinter as tk
    from tkinter import messagebox
    from tkinter import filedialog
    from tkinter import simpledialog as simpleDialog
    from xml.etree import ElementTree
else:
#    from Tkinter import *
    import Tkinter as tk
    import tkMessageBox as messagebox
    import tkFileDialog as filedialog
    import tkSimpleDialog as simpleDialog
    from xml.etree import cElementTree as ElementTree
### ----------------------------------------------------------------------
### Local modules

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Classes"))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Enums"))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Forms"))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Utils"))


from CEnums import *
from CUtils import *

from CBuilding import *
from CZone import *
from CPresence import *
from CWindows import *
from CWindow import *
from CShades import *
from CShade import *
from CLights import *
from CAgentHeatGains import *
from CHeating import *

from CSimulation import *

from FEmpty import *
from FLog import *
from FConfiguration import *
from FRun import *
from FPlots import *
from FBuilding import *
from FZone import *
from FOccupant import *
from FPresence import *
from FWindows import *
from FWindow import *
from FShades import *
from FShade import *
from FLights import *
from FAgentHeatGains import *
from FHeating import *
from FOccupantTemplates import *

class App():
    ## \brief Create main tool bar
    # Create the main tool bar
    # \param self.
    # \param parent. Parent widget
    def createMainToolbar(self, parent):
        toolBarFrame = tk.Frame(parent, bd=1, relief=tk.RAISED)

        btnNew = Utils.UI.Controls.ImageButton(toolBarFrame, Utils.Resources.Icons.file_o_16_0_333333, self.newProject, "Start new simulation configuration")
        btnNew.pack(side=tk.LEFT, padx=2, pady=2)

        btnOpen = Utils.UI.Controls.ImageButton(toolBarFrame, Utils.Resources.Icons.folder_open_o_16_0_333333, self.openProject, "Open simulation configuration file")
        btnOpen.pack(side=tk.LEFT, padx=2, pady=2)

        btnSave = Utils.UI.Controls.ImageButton(toolBarFrame, Utils.Resources.Icons.save_16_0_333333, self.saveProject, "Save simulation configuration")
        btnSave.pack(side=tk.LEFT, padx=2, pady=2)

        sep = ttk.Separator(toolBarFrame, orient="vertical")
        sep.pack(side=tk.LEFT, fill=tk.Y)

        btnAppendZone = Utils.UI.Controls.ImageButton(toolBarFrame, Utils.Resources.Icons.cube_16_0_333333, self.appendZone, "New zone")
        btnAppendZone.pack(side=tk.LEFT, padx=2, pady=2)

        btnAppendOccupant = Utils.UI.Controls.ImageButton(toolBarFrame, Utils.Resources.Icons.user_o_16_0_333333, self.appendOccupant, "New occupant")
        btnAppendOccupant.pack(side=tk.LEFT, padx=2, pady=2)

        return toolBarFrame
    # end of createMainToolbar

    ## \brief Create status bar
    # Create status
    # \param self.
    # \param parent. Parent widget
    def createStatusBar(self, parent):
        statusBarFrame = tk.Frame(parent, bd=1, relief='sunken')
        statusBarFrame.grid_rowconfigure(0, weight=1)
        statusBarFrame.grid_columnconfigure(0, weight=0)
        statusBarFrame.grid_columnconfigure(1, weight=0)

        messageFrame = tk.Frame(statusBarFrame)
        messageFrame.grid(row=0, column=1, sticky='nswe')
        progressBarFrame = tk.Frame(statusBarFrame)
        progressBarFrame.grid(row=0, column=0, sticky='nswe')

        self.progressBar = ttk.Progressbar(progressBarFrame, orient="horizontal", mode="determinate", length=400)
        self.progressBar.pack(side='left')
        self.progressBar["value"] = 0
        self.progressBar["maximum"] = 100

        self.sbMessage = tk.Label(messageFrame, anchor='w')
        self.sbMessage.config(text="")
        self.sbMessage.pack(side='left')
        return statusBarFrame
    # end of createStatusBar
#
    ## \brief Close application
    # Destroy all resources before closing the application
    # \param self.
    def exitCallback(self):
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            self.freeResources()
            self.master.destroy()
            sys.exit(1)
        return
    # end of exitCallback

    ## \brief Destroy forms and widgets
    # Destroy forms and widgets
    # \param self.
    def freeResources(self):
        #self.bringForm(Utils.Constants.emptyGUID, True)
        self.tvwBuildings.delete(*self.tvwBuildings.get_children())
        self.tvwModels.delete(*self.tvwModels.get_children())
        for itemKey in list(self.pItems.keys()): # updated 18.10.2021 daps
            del self.pItems[itemKey]
        self.pItems.clear()
        return
    # end of freeResources

    ## \brief Reset data structures
    # Reset data structures
    # \param self.
    def resetProject(self, loadDefaultNoMASSModels=False):
        self.simulation = Simulation()
        self.fConfiguration.loadObjSimulation(self.simulation)
        # self.createForms()
        # self.initTabEdit()
        self.freeResources()
        self.initBuilding()
        if loadDefaultNoMASSModels:
            self.loadModels()

        self.fEmpty.title=""
        self.fEmpty.show()
        self.refreshTabEdit()
        # self.log(str(self.appCurrentState))
        self.sbmessage("Restarted!")
        self.sbmessage("")
        return
    # end of resetProject
#
    
    ## \brief Create a new empty project
    # Create a new empty project
    # \param self.
    def newProject(self):
        if messagebox.askyesno("New", "Are you sure to delete the current configuration and start a new one ?"):
            self.resetProject(True)
            self.status = typeOfAppStatus.IDLE
        # self.log(str(self.appCurrentState))
        self.sbmessage("New project!!")
        return
    # end of NewProject

    def refreshTabEdit(self, newHeight=None):
        height = self.tabEdit.height
        if newHeight is not None:
            height = newHeight
        self.tabEdit.update()
        self.tabEdit.updateViewPort(self.tabEdit.width, height)
        return
    # end of refreshTabEdit
#
    ## \brief Open a project
    # Open a project
    # \param self.
    def openProject(self):
        filename = filedialog.askopenfilename(title = "Open XML simulation config file...", defaultextension=".xml", filetypes = (("all files","*.*"),("xml files","*.xml")))
        if filename is None or len(str(filename).strip()) == 0:
            return
        self.resetProject()
        
        self.simulation = Simulation()
        self.simulation.loadFromFile(filename)
        # self.loadUIfromSimulationConfig()
        self.loadConfiguration()
        self.log("Simulation loaded from file")
        return
    # end of openProject

    ## \brief Save current project
    # Save current project
    # \param self.
    def saveProject(self):
        # validate zones, agents, windows and shade devices
        pZones = self.getListOfItemsByType(typeOfClass.BUILDING_ZONE)
        pOccupants = self.getListOfItemsByType(typeOfClass.BUILDING_OCCUPANTTEMPLATE)

        if pZones is None or len(pZones)==0:
            messagebox.showerror(title='Error!', message="The building has no zones")
            return None
        if pOccupants is None or len(pOccupants)==0:
            messagebox.showerror(title='Error!', message="The building has no occupants")
            return None

        currentFilename = ""
        currentPath = Utils.Config.getAppLocation()
        if self.simulation.filename != "":
            currentFilename = Utils.IO.filename(self.simulation.filename)
            currentPath = Utils.IO.folderPath(currentFilename)
        filename = filedialog.asksaveasfilename(title = "Write Simulation Config file...", defaultextension=".xml", filetypes = (("xml files","*.xml"), ("all files","*.*")), initialdir=currentPath, initialfile=currentFilename)
        if filename is None or len(str(filename).strip()) == 0:
            return None

        if not os.path.exists(Utils.IO.folderPath(filename)):
            return None

        self.simulation.outputVariables = ""                                   # Clean variables, update 2019

        saveOutput = self.saveConfiguration(filename)
        if saveOutput is not None and saveOutput == True:
            #self.sbmessage("The project has been saved!")
            self.sbmessage("")
            return filename
        else:
            self.sbmessage("Error while writing SimulationConfig.xml file!")
            return None
        return
    # end of saveProject

    def saveConfiguration(self, filename, sessionID=None):
        if self.simulation.sessionID == Utils.Constants.emptyGUID:
            self.simulation.sessionID = str(uuid.uuid4())

        # validate zones, agents, windows and shade devices
        pZones = self.getListOfItemsByType(typeOfClass.BUILDING_ZONE)
        pOccupants = self.getListOfItemsByType(typeOfClass.BUILDING_OCCUPANTTEMPLATE)

        if pZones is None or len(pZones)==0:
            messagebox.showerror(title='Error!', message="The building has no zones")
            return False
        if pOccupants is None or len(pOccupants)==0:
            messagebox.showerror(title='Error!', message="The building has no occupants")
            return False

        # update filename
        self.simulation.filename = filename

        # update general settings
        self.simulation.typeOfBuilding = self.fConfiguration.typeOfBuilding
        self.simulation.area = self.fConfiguration.area
        self.simulation.numberOfOccupants = self.fConfiguration.numberOfOccupants
        self.simulation.seed = self.fConfiguration.seed
        self.simulation.timeStepsPerHour = self.fConfiguration.timeStepsPerHour
        self.simulation.beginMonth = self.fConfiguration.beginMonth
        self.simulation.endMonth = self.fConfiguration.endMonth
        self.simulation.beginDay = self.fConfiguration.beginDay
        self.simulation.endDay = self.fConfiguration.endDay
        self.simulation.learn = self.fConfiguration.learn
        self.simulation.save = self.fConfiguration.save
        self.simulation.eplusVersion = self.fConfiguration.eplusVersion
        self.simulation.numberOfReplicates = self.fConfiguration.numberOfReplicates
        self.simulation.numberOfReplicatesRandom = self.fConfiguration.numberOfReplicatesRandom

        # update resource files and output directories
        self.simulation.idfFilename = self.fRun.idfFilename
        self.simulation.weatherFilename = self.fRun.weatherFilename
        self.simulation.outputDirectory = self.fRun.outputDirectory
        self.simulation.eplusLocation = self.fRun.eplusLocation

        self.simulation.randomWindow = self.fRun.randomWindow
        self.simulation.randomShade = self.fRun.randomShade
        
        self.simulation.attachDayCtrl = self.fRun.attachDayCtrl
        self.simulation.attachWinState0 = self.fRun.attachWinState0

        # update building (zones, agents) and stochastic models
        self.simulation.building.clearZones()
        self.simulation.building.clearOccupants()
        self.simulation.models.windows.clear()
        self.simulation.models.shades.clear()

        insBuilding = self.getItemByType(typeOfClass.BUILDING)
        self.simulation.building.id = insBuilding.ID
        self.simulation.building.name = insBuilding.name

        for zone in pZones:
            print("zone", zone)
            self.simulation.building.zones.append(Simulation.Building.Zone(
                id = zone.ID,
                name = zone.name,
                activities = zone.activities,
                isGroundFloor = zone.groundFloor,
                windowCount = zone.windowCount,
                floorArea = zone.floorArea
            ))

        i = 1
        for occupant in pOccupants:
            _occupant = occupant.occupants[0]
            #print("   occupant %s" % (str(i)), _occupant.windowId, _occupant.window, _occupant.shadeId, _occupant.shade, _occupant.activityId)
            self.simulation.building.occupants.append(
                Simulation.Building.Occupant(
                    id=i,
                    name=occupant.name,
                    description=occupant.description,
                    categoryID=occupant.categoryID,
                    category=occupant.category,
                    regionID=occupant.regionID,
                    region=occupant.region,
                    sectorID=occupant.sectorID,
                    sector=occupant.sector,
                    zoneId=_occupant.zoneId,
                    zone=_occupant.zoneId,
                    power=_occupant.power,
                    windowId=_occupant.windowId,
                    window=_occupant.window,
                    shadeId=_occupant.shadeId,
                    shade=_occupant.shade,
                    activityId=_occupant.activityId,
                    sex=_occupant.sex,
                    familyID=_occupant.familyID,
                    educationID=_occupant.educationID,
                    ageGroup=_occupant.ageGroup,
                    ownComputer=_occupant.ownComputer,
                    isRetired=_occupant.isRetired,
                    isMarried=_occupant.isMarried,
                    isUnEmployed=_occupant.isUnEmployed
                )
            )
            i += 1


        insPresence = self.getItemByType(typeOfClass.MODEL_PRESENCE)
        insWindows = self.getItemByType(typeOfClass.MODEL_WINDOWS)
        insShades = self.getItemByType(typeOfClass.MODEL_SHADES)
        insLights = self.getItemByType(typeOfClass.MODEL_LIGHTS)
        insAHG = self.getItemByType(typeOfClass.MODEL_AGENTHEATGAINS)
        insHeating = self.getItemByType(typeOfClass.MODEL_HEATING)

        pWindows = self.getListOfItemsByType(typeOfClass.MODEL_WINDOW)
        pShades = self.getListOfItemsByType(typeOfClass.MODEL_SHADE)

        for element in pWindows:
            self.simulation.models.windows.append(Simulation.NoMASSModels.Windows.Window(
                id = element.ID,
                name = element.name,
                aop = element.aop,
                bopout = element.bopout,
                shapeop = element.shapeop,
                a01arr = element.a01arr,
                b01inarr = element.b01inarr,
                b01outarr = element.b01outarr,
                b01absprevarr = element.b01absprevarr,
                b01rnarr = element.b01rnarr,
                a01int = element.a01int,
                b01inint = element.b01inint,
                b01outint = element.b01outint,
                b01presint = element.b01presint,
                b01rnint = element.b01rnint,
                a01dep = element.a01dep,
                b01outdep = element.b01outdep,
                b01absdep = element.b01absdep,
                b01gddep = element.b01gddep,
                a10dep = element.a10dep,
                b10indep = element.b10indep,
                b10outdep = element.b10outdep,
                b10absdep = element.b10absdep,
                b10gddep = element.b10gddep,
            ))

        for element in pShades:
            self.simulation.models.shades.append(Simulation.NoMASSModels.Shades.Shade(
                id = element.ID,
                name = element.name,
                a01arr = element.a01arr,
                b01inarr = element.b01inarr,
                b01sarr = element.b01sarr,
                a10arr = element.a10arr,
                b10inarr = element.b10inarr,
                b10sarr = element.b10sarr,
                a01int = element.a01int,
                b01inint = element.b01inint,
                b01sint = element.b01sint,
                a10int = element.a10int,
                b10inint = element.b10inint,
                b10sint = element.b10sint,
                afullraise = element.afullraise,
                boutfullraise = element.boutfullraise,
                bsfullraise = element.bsfullraise,
                bsfulllower = element.bsfulllower,
                boutfulllower = element.boutfulllower,
                afulllower = element.afulllower,
                aSFlower = element.aSFlower,
                bSFlower = element.bSFlower,
                shapelower = element.shapelower
            ))

        self.simulation.models.presence.enabled = insPresence.enabled
        self.simulation.models.windows.enabled = insWindows.enabled
        self.simulation.models.shades.enabled = insShades.enabled
        self.simulation.models.lights.enabled = insLights.enabled
        self.simulation.models.agentHeatGains.enabled = insAHG.enabled
        self.simulation.models.heating.enabled = insHeating.enabled

        self.simulation.saveXML()
        return True
    # end of saveConfiguration
    
    def loadConfiguration(self):
        print("self.simulation", self.simulation, self.simulation.__dict__)
        # general simulation config
        self.fConfiguration.loadObjSimulation(self.simulation)
        
        self.tvwBuildings.selection_set(self.tvwBuildings.tag_has(typeOfClass.BUILDING_ZONES))
        insZones = self.tvwBuildings.selection()
        # building, zones and occupants
        for zone in self.simulation.building.zones:
            newZone = CZone(id=str(uuid.uuid4()),
                            name=zone.name,
                            activities=zone.activities,
                            groundFloor=zone.isGroundFloor,
                            windowCount=zone.windowCount,
                            floorArea=zone.floorArea)
            self.pItems[newZone.UUID] = newZone
    
            # aggregate to the treeview
            itemZone = self.tvwBuildings.insert(insZones, tk.END, text=newZone.name, values=(typeOfClass.BUILDING_ZONE, newZone.UUID), tags=typeOfClass.BUILDING_ZONE)
            self.log("appendZone (%s)" % (newZone.name))
        
        self.tvwBuildings.selection_set(self.tvwBuildings.tag_has(typeOfClass.BUILDING_OCCUPANTS))
        insOccupants = self.tvwBuildings.selection()
        
        # Load models and activate the selected models only !!!
        self.loadModels()
        print("simulation.models.presence.enabled:", self.simulation.models.presence.enabled)
        print("simulation.models.windows.enabled:", self.simulation.models.windows.enabled)
        print("simulation.models.shades.enabled:", self.simulation.models.shades.enabled)
        print("simulation.models.lights.enabled:", self.simulation.models.lights.enabled)
        print("simulation.models.agentHeatGains.enabled:", self.simulation.models.agentHeatGains.enabled)
        print("simulation.models.heating.enabled:", self.simulation.models.heating.enabled)
        
        insPresence = self.getItemByType(typeOfClass.MODEL_PRESENCE)
        insWindows = self.getItemByType(typeOfClass.MODEL_WINDOWS)
        insShades = self.getItemByType(typeOfClass.MODEL_SHADES)
        insLights = self.getItemByType(typeOfClass.MODEL_LIGHTS)
        insAHG = self.getItemByType(typeOfClass.MODEL_AGENTHEATGAINS)
        insHeating = self.getItemByType(typeOfClass.MODEL_HEATING)
        
        insPresence.enabled = self.simulation.models.presence.enabled
        insWindows.enabled = self.simulation.models.windows.enabled
        insShades.enabled = self.simulation.models.shades.enabled
        insLights.enabled = self.simulation.models.lights.enabled
        insAHG.enabled = self.simulation.models.agentHeatGains.enabled
        insHeating.enabled = self.simulation.models.heating.enabled
        
        # load execution params
        self.fRun._idfFilename.set(self.simulation.idfFilename)
        self.fRun._weatherFilename.set(self.simulation.weatherFilename)
        self.fRun._outputDirectory.set(self.simulation.outputDirectory)
        self.fRun._eplusLocation.set(self.simulation.eplusLocation)
        
        self.fRun._attachDayCtrl.set(self.simulation.attachDayCtrl)
        self.fRun._attachWinState0.set(self.simulation.attachWinState0)
        
        return True
    # end of loadConfiguration

    def newItemNameExist(self, typeOfItem, itemName, itemID=Utils.Constants.emptyGUID, parentID=None):
        items = []
        if typeOfItem == typeOfClass.BUILDING_ZONE:
            items = getListOfItemsByType(typeOfClass.BUILDING_ZONE)
        else:
            if typeOfItem == typeOfClass.BUILDING_OCCUPANTTEMPLATE:
                items = getListOfItemsByType(typeOfClass.BUILDING_OCCUPANTTEMPLATE)

        if not items:
             return False

        for item in items:
            if item.name.lower() == itemName.lower():
                if typeOfItem == typeOfClass.BUILDING_ZONE and (itemID == Utils.Constants.emptyGUID or (itemID != Utils.Constants.emptyGUID and item.ID != itemID)):
                    return True

                if typeOfItem == typeOfClass.BUILDING_OCCUPANTTEMPLATE and (itemID == Utils.Constants.emptyGUID or (itemID != Utils.Constants.emptyGUID and item.UUID != itemID)):
                    return True
        return False
    # end of newItemNameExist
    
    ## \brief Append zone to the building
    # Append zone to the building
    # \param self.
    def appendZone(self):
        # verify that selected node equals "Building"
        if self.tvwBuildings.selection() == None or self.tvwBuildings.selection() == '':
            return

        node = self.tvwBuildings.selection()[0]

        if len(self.tvwBuildings.item(node)["tags"]) != 1:
            return

        typeOfObject = self.tvwBuildings.item(node)["values"][0]
        key = self.tvwBuildings.item(node)["values"][1]

        if typeOfObject != typeOfClass.BUILDING_ZONES:
            return

        zoneName = simpleDialog.askstring("Zone name", "Name", initialvalue="newZone")
        if not zoneName or (zoneName is not None and len(str(zoneName).strip())==0):
            return

        zoneName = zoneName.strip()
        if self.newItemNameExist(typeOfClass.BUILDING_ZONE, zoneName):
            messagebox.showerror(title='Error!', message="Name '" + zoneName + "' is already in use")
            return

        # append zone to the building
        newZone = CZone(id=str(uuid.uuid4()),
                        name=zoneName,
                        activities='',
                        groundFloor=False,
                        windowCount=0,
                        floorArea=0)
        self.pItems[newZone.UUID] = newZone

        # aggregate to the treeview
        itemZone = self.tvwBuildings.insert(node, tk.END, text=newZone.name, values=(typeOfClass.BUILDING_ZONE, newZone.UUID), tags=typeOfClass.BUILDING_ZONE)
        self.log("appendZone (%s)" % (newZone.name))
        return itemZone
    # end of appendZone

    ## \brief Append occupant to the building
    # Append occupant to the building
    # \param self.
    def appendOccupant(self):
        # verify that selected node equals "Building"
        if self.tvwBuildings.selection() == None or self.tvwBuildings.selection() == '':
            return

        node = self.tvwBuildings.selection()[0]

        if len(self.tvwBuildings.item(node)["tags"]) != 1:
            return

        typeOfObject = self.tvwBuildings.item(node)["values"][0]
        key = self.tvwBuildings.item(node)["values"][1]

        if typeOfObject != typeOfClass.BUILDING_OCCUPANTS:
            return

        pZones = getListOfItemsByType(typeOfClass.BUILDING_ZONE)
        if pZones is None:
            messagebox.showerror(title='Error!', message="There are no zones in the building to allocate occupants!")
            return

        if len(pZones) == 0:
            messagebox.showerror(title='Error!', message="There are no zones in the building to allocate occupants!")
            return

        # popup the occupant selector window
        dlg = FrmOccupantTemplates(self.master, pZones)
        self.master.wait_window(dlg.top)
        if dlg.error:
            messagebox.showerror(title='Error!', message=dlg.message)
            return

        if dlg.template.UUID == Utils.Constants.emptyGUID:
            return
        
        # append agents to the simulation config
        i = 1
        for occupant in dlg.template.occupants:
            newLabel = dlg.template.name + "_" + str(i)

            # update occupant name
            occupant.name = newLabel
            occupant.zoneId = pZones[0].name
            occupant.zone = pZones[0].name

            newOccupantTemplate = COccupantTemplate(
                            dlg.template.ID,
                            newLabel, #dlg.template.name,
                            dlg.template.description,
                            dlg.template.categoryID,
                            dlg.template.category,
                            dlg.template.regionID,
                            dlg.template.region,
                            dlg.template.sectorID,
                            dlg.template.sector)
            newOccupantTemplate.occupants.append(occupant)

            # append agent item to the treeview
            self.pItems[newOccupantTemplate.UUID] = newOccupantTemplate
            # aggregate to the treeview
            itemOccupant = self.tvwBuildings.insert(node, tk.END, text=occupant.name, values=(typeOfClass.BUILDING_OCCUPANTTEMPLATE, newOccupantTemplate.UUID), tags=typeOfClass.BUILDING_OCCUPANTTEMPLATE)
            i += 1
        self.log("appendOccupant (%s)" % (occupant.name))
        return itemOccupant
    # end of appendOccupant

    ## \brief Load data form
    # Load data form
    # \param self.
    def TreeView_OnNodeSelect(self, event, treeview):
        if treeview.selection() == None or treeview.selection() == '':
            return

        node = treeview.selection()[0]

        if len(treeview.item(node)["tags"]) != 1:
            return

        typeOfObject = treeview.item(node)["values"][0]
        key = str(treeview.item(node)["values"][1])

        if typeOfObject == typeOfClass.BUILDING:
            self.fBuilding.load(self.pItems[key]._id,
                self.pItems[key]._name,
                True)
        else:
            if typeOfObject == typeOfClass.BUILDING_ZONE:
                self.fZone.load(
                    id = self.pItems[key]._id,
                    name = self.pItems[key]._name,
                    activities = self.pItems[key]._activities,
                    groundFloor = self.pItems[key]._groundFloor,
                    windowCount = self.pItems[key]._windowCount,
                    floorArea = self.pItems[key]._floorArea,
                    show=True,
                    enabled=True)
            else:
                if typeOfObject == typeOfClass.BUILDING_OCCUPANTTEMPLATE:
                    self.fOccupant.load(
                        id = self.pItems[key]._id,
                        name = self.pItems[key]._name,
                        description = self.pItems[key]._description,
                        categoryID = self.pItems[key]._categoryID,
                        category = self.pItems[key]._category,
                        regionID = self.pItems[key]._regionID,
                        region = self.pItems[key]._region,
                        sectorID = self.pItems[key]._sectorID,
                        sector = self.pItems[key]._sector,
                        occupants = self.pItems[key]._occupants,
                        # zones=self.getListOfItemsByType(typeOfClass.BUILDING_ZONE),
                        zones=self.getListOfZones(),
                        show=True,
                        enabled=True)
                else:
                    if typeOfObject == typeOfClass.MODEL_PRESENCE:
                        self.fPresence.load(self.pItems[key]._enabled, True)
                    else:
                        if typeOfObject == typeOfClass.MODEL_WINDOWS:
                            self.fWindows.load(self.pItems[key]._enabled, True)
                        else:
                            if typeOfObject == typeOfClass.MODEL_WINDOW:
                                self.fWindow.load(
                                    id = self.pItems[key]._id,
                                    name = self.pItems[key]._name,
                                    aop = self.pItems[key]._aop,
                                    bopout = self.pItems[key]._bopout,
                                    shapeop = self.pItems[key]._shapeop,
                                    a01arr = self.pItems[key]._a01arr,
                                    b01inarr = self.pItems[key]._b01inarr,
                                    b01outarr = self.pItems[key]._b01outarr,
                                    b01absprevarr = self.pItems[key]._b01absprevarr,
                                    b01rnarr = self.pItems[key]._b01rnarr,
                                    a01int = self.pItems[key]._a01int,
                                    b01inint = self.pItems[key]._b01inint,
                                    b01outint = self.pItems[key]._b01outint,
                                    b01presint = self.pItems[key]._b01presint,
                                    b01rnint = self.pItems[key]._b01rnint,
                                    a01dep = self.pItems[key]._a01dep,
                                    b01outdep = self.pItems[key]._b01outdep,
                                    b01absdep = self.pItems[key]._b01absdep,
                                    b01gddep = self.pItems[key]._b01gddep,
                                    a10dep = self.pItems[key]._a10dep,
                                    b10indep = self.pItems[key]._b10indep,
                                    b10outdep = self.pItems[key]._b10outdep,
                                    b10absdep = self.pItems[key]._b10absdep,
                                    b10gddep = self.pItems[key]._b10gddep,
                                    show=True)
                            else:
                                if typeOfObject == typeOfClass.MODEL_SHADES:
                                    self.fShades.load(self.pItems[key]._enabled, True)
                                else:
                                    if typeOfObject == typeOfClass.MODEL_SHADE:
                                        self.fShade.load(
                                            id = self.pItems[key]._id,
                                            name = self.pItems[key]._name,
                                            a01arr = self.pItems[key]._a01arr,
                                            b01inarr = self.pItems[key]._b01inarr,
                                            b01sarr = self.pItems[key]._b01sarr,
                                            a10arr = self.pItems[key]._a10arr,
                                            b10inarr = self.pItems[key]._b10inarr,
                                            b10sarr = self.pItems[key]._b10sarr,
                                            a01int = self.pItems[key]._a01int,
                                            b01inint = self.pItems[key]._b01inint,
                                            b01sint = self.pItems[key]._b01sint,
                                            a10int = self.pItems[key]._a10int,
                                            b10inint = self.pItems[key]._b10inint,
                                            b10sint = self.pItems[key]._b10sint,
                                            afullraise = self.pItems[key]._afullraise,
                                            boutfullraise = self.pItems[key]._boutfullraise,
                                            bsfullraise = self.pItems[key]._bsfullraise,
                                            bsfulllower = self.pItems[key]._bsfulllower,
                                            boutfulllower = self.pItems[key]._boutfulllower,
                                            afulllower = self.pItems[key]._afulllower,
                                            aSFlower = self.pItems[key]._aSFlower,
                                            bSFlower = self.pItems[key]._bSFlower,
                                            shapelower = self.pItems[key]._shapelower,
                                            show=True)
                                    else:
                                        if typeOfObject == typeOfClass.MODEL_LIGHTS:
                                            self.fLights.load(self.pItems[key]._enabled, True)
                                        else:
                                            if typeOfObject == typeOfClass.MODEL_AGENTHEATGAINS:
                                                self.fAgentHeatGains.load(self.pItems[key]._enabled, True)
                                            else:
                                                if typeOfObject == typeOfClass.MODEL_HEATING:
                                                    self.fHeating.load(self.pItems[key]._enabled, True)
                                                else:
                                                    self.fEmpty.load()
                                                    self.refreshTabEdit()
        return
    # end of TreeView_OnNodeSelect

    def tvwBuildings_OnContextMenu(self, event):
        selection = self.tvwBuildings.identify('row', event.x, event.y)
        try:
            self.tvwBuildings.selection_set(selection)
            typeOfObject = self.tvwBuildings.item(selection)["values"][0]
            key = str(self.tvwBuildings.item(selection)["values"][1])
            if typeOfObject != typeOfClass.BUILDING_ZONE and typeOfObject != typeOfClass.BUILDING_OCCUPANTTEMPLATE:
                return
            self.cmenuBuildings.selection = self.tvwBuildings.selection_set(selection)
            self.cmenuBuildings.tk_popup(event.x_root, event.y_root)
        except:
            return

        return
    # end of tvwBuildings_OnContextMenu

    def updateOccupantZoneID(self, key, newName):
        insOldZone = self.pItems[key]
        self.fOccupant.updateZoneList(self.getListOfZones())

        pOccupants = getListOfItemsByType(typeOfClass.BUILDING_OCCUPANTTEMPLATE)
        if pOccupants is None or len(pOccupants) == 0:
            return

        for occupant in pOccupants:
            if occupant.occupants[0].zoneId.strip().lower() == insOldZone.name.strip().lower():
                occupant.occupants[0].zoneId = newName
        return

    def tvwBuildings_OnRenameItem(self, event=None):
        node = self.tvwBuildings.selection()[0]
        if node is None:
            return

        typeOfObject = self.tvwBuildings.item(node)["values"][0]
        key = str(self.tvwBuildings.item(node)["values"][1])

        if typeOfObject != typeOfClass.BUILDING_ZONE and typeOfObject != typeOfClass.BUILDING_OCCUPANTTEMPLATE:
            return

        insObject = self.pItems[key]

        newName = simpleDialog.askstring("%s name" % ("Zone" if typeOfObject == typeOfClass.BUILDING_ZONE else "Occupant"), "Name", initialvalue=insObject.name)
        if not newName or (newName is not None and len(str(newName).strip())==0):
            return

        newName = newName.strip()
        if self.newItemNameExist(typeOfObject, newName, insObject.UUID):
            messagebox.showerror(title='Error!', message="Name '" + newName + "' is already in use")
            return

        if typeOfObject == typeOfClass.BUILDING_ZONE:
            self.updateOccupantZoneID(key, newName)

        self.pItems[key].name = newName
        self.tvwBuildings.item(node, text=self.pItems[key].name, values=self.tvwBuildings.item(node)["values"], tags=self.tvwBuildings.item(node)["tags"])
        return
    # end of tvwBuildings_OnRenameItem

    def tvwBuildings_OnDoubleClickItem(self, event=None):
        self.tvwBuildings_OnRenameItem(event)
        return
    # end of tvwBuildings_OnDoubleClickItem

    def existsOccupantsInZone(self, zoneId):
        insZone = self.pItems[zoneId]
        pOccupants = getListOfItemsByType(typeOfClass.BUILDING_OCCUPANTTEMPLATE)
        if pOccupants is None or len(pOccupants) == 0:
            return False

        for occupant in pOccupants:
            if occupant.occupants[0].zoneId.strip().lower() == insZone.name.strip().lower():
                return True
        return False
    # end of existsOccupantsInZone

    def tvwBuildings_OnDeleteItem(self, event=None):
        node = self.tvwBuildings.selection()[0]
        if node is None:
            return

        typeOfObject = self.tvwBuildings.item(node)["values"][0]
        key = str(self.tvwBuildings.item(node)["values"][1])
        parent = self.tvwBuildings.parent(node)
        if typeOfObject != typeOfClass.BUILDING_ZONE and typeOfObject != typeOfClass.BUILDING_OCCUPANTTEMPLATE:
            return

        if not messagebox.askyesno("New", "Are you sure to delete the selected %s ?" % ("zone" if typeOfObject == typeOfClass.BUILDING_ZONE else "occupant")):
            return

        # remove item from dictionary and treeview
        # validate there are no occupants in the current zone
        isValid = True
        errorMessage = ""

        if typeOfObject == typeOfClass.BUILDING_ZONE and self.existsOccupantsInZone(key):
            isValid = False
            errorMessage = "There are occupants in the selected zone"

        if not isValid:
            messagebox.showerror(title='Error!', message=errorMessage)
            return False

        try:
            del self.pItems[key]

            self.tvwBuildings.delete(node)
            if parent:
                self.tvwBuildings.selection_set(parent)
                self.tvwBuildings.focus_set()
                self.tvwBuildings.focus(parent)
            return True
        except:
            return False

        return False
    # end of tvwBuildings_OnDeleteItem

    def updateProgressBar(self, value):
        self.progressBar["value"] = value
        self.progressBar.update_idletasks()
        return
    # end of updateProgressBar

    def sbmessage(self, message):
        maxLength = 50
        if len(message) > maxLength:
         message = message[0:maxLength:1]
         message += "..."
        self.sbMessage.config(text=message)
        return
    # end of sbmessage

    def log(self, message):
        self.fLog.write(message)
    # end of log

    def appState(self, value=None):
        if value is not None:
            self.appCurrentState = value
        return self.appCurrentState
    # end of appState
    
    def refreshGUI(self):
        root.update()
        return

    def createForms(self):
        self.fEmpty = FrmEmpty(self.tabEdit.innerframe)
        self.fLog = FrmLog(self.tabLog)
        self.fConfiguration = FrmConfiguration(self.tabConfiguration.innerframe, self.simulation)
        self.fRun = FrmRun(self, self.tabRun.innerframe, self.simulation)
        self.fPlots = FrmPlots(self, self.tabPlots.innerframe, self.simulation)

        self.fBuilding = FrmBuilding(self, self.tabEdit.innerframe)
        self.fZone = FrmZone(self, self.tabEdit.innerframe)
        self.fOccupant = FrmOccupant(self, self.tabEdit.innerframe)

        self.fPresence = FrmPresence(self, self.tabEdit.innerframe)
        self.fWindows = FrmWindows(self, self.tabEdit.innerframe)
        self.fShades = FrmShades(self, self.tabEdit.innerframe)
        self.fLights = FrmLights(self, self.tabEdit.innerframe)
        self.fAgentHeatGains = FrmAgentHeatGains(self, self.tabEdit.innerframe)
        self.fHeating = FrmHeating(self, self.tabEdit.innerframe)

        self.fWindow = FrmWindow(self, self.tabEdit.innerframe)
        self.fShade = FrmShade(self, self.tabEdit.innerframe)
        return
    # end of createForms

    def initTabEdit(self):
        self.fEmpty.title = ""
        self.fEmpty.Frame.tkraise()
        self.refreshTabEdit()
        return
    # end of initTabEdit

    def getListOfItemsByType(self, typeOfClass):
        output = []
        for _key, _value in self.pItems.items():
            if _value.type == typeOfClass:
                output.append(_value)

        if len(output) == 0:
            return None

        return output
    # end of getListOfItemsByType

    def getItemByType(self, typeOfClass):
        for _key, _value in self.pItems.items():
            if _value.type == typeOfClass:
                return _value
        return None
    # end of getItemByType

    def getListOfZones(self):
        output={}
        pZones = self.getListOfItemsByType(typeOfClass.BUILDING_ZONE)
        if pZones is None or len(pZones)==0:
            return output
        for zone in pZones:
            output[zone.UUID] = zone.name

        return output

    def initBuilding(self):
        insBuilding = self.getListOfItemsByType(typeOfClass.BUILDING)
        if insBuilding is not None:
            self.tvwBuildings.delete(*self.tvwBuildings.get_children())
            del self.pItems[insBuilding.UUID]

        insBuild = CBuilding(0, "Building")
        self.pItems[insBuild.UUID] = insBuild
        self.oBuilding = self.tvwBuildings.insert("", "end", text="Building", values=[typeOfClass.BUILDING, insBuild.UUID], tags=typeOfClass.BUILDING, open=True)
        self.oBuildingZones = self.tvwBuildings.insert(self.oBuilding, "end", text="Zones", values=[typeOfClass.BUILDING_ZONES, Utils.Constants.emptyGUID], tags=typeOfClass.BUILDING_ZONES, open=True)
        self.oBuildingOccupants = self.tvwBuildings.insert(self.oBuilding, "end", text="Occupants", values=[typeOfClass.BUILDING_OCCUPANTS, Utils.Constants.emptyGUID], tags=typeOfClass.BUILDING_OCCUPANTS, open=True)
        return
    # end of initBuilding

    def loadModels(self):
        # aggregate the NoMASS models to the collection of items
        self.oModels = self.tvwModels.insert("", "end", text="Models", values=[typeOfClass.MODELS, ""], tags=typeOfClass.MODELS, open=True)
        insPresence = CPresence(enabled=True)
        insWindows = CWindows(enabled=True)
        insShades = CShades(enabled=True)
        insLights = CLights(enabled=True)
        insAHG = CAgentHeatGains(enabled=True)
        insHeating = CHeating(enabled=True)
        self.pItems[insWindows.UUID] = insWindows
        self.pItems[insShades.UUID] = insShades
        self.pItems[insLights.UUID] = insLights
        self.pItems[insPresence.UUID] = insPresence
        self.pItems[insAHG.UUID] = insAHG
        self.pItems[insHeating.UUID] = insHeating

        self.oPresence = self.tvwModels.insert(self.oModels, "end", text="Presence", values=[typeOfClass.MODEL_PRESENCE, insPresence.UUID], tags=typeOfClass.MODEL_PRESENCE, open=True)
        self.oWindows = self.tvwModels.insert(self.oModels, "end", text="Windows", values=[typeOfClass.MODEL_WINDOWS, insWindows.UUID], tags=typeOfClass.MODEL_WINDOWS, open=False)
        self.oShades = self.tvwModels.insert(self.oModels, "end", text="Shades", values=[typeOfClass.MODEL_SHADES, insShades.UUID], tags=typeOfClass.MODEL_SHADES, open=False)
        self.oLights = self.tvwModels.insert(self.oModels, "end", text="Lights", values=[typeOfClass.MODEL_LIGHTS, insLights.UUID], tags=typeOfClass.MODEL_LIGHTS, open=True)
        self.oAHG = self.tvwModels.insert(self.oModels, "end", text="Agent Heat Gains", values=[typeOfClass.MODEL_AGENTHEATGAINS, insAHG.UUID], tags=typeOfClass.MODEL_AGENTHEATGAINS, open=True)
        self.oHeating = self.tvwModels.insert(self.oModels, "end", text="Heating", values=[typeOfClass.MODEL_HEATING, insHeating.UUID], tags=typeOfClass.MODEL_HEATING, open=True)
        self.fPresence.load(insPresence.enabled)
        self.fWindows.load(insWindows.enabled)
        self.fShades.load(insShades.enabled)
        self.fLights.load(insLights.enabled)
        self.fAgentHeatGains.load(insAHG.enabled)
        self.fHeating.load(insHeating.enabled)

        # load xml file with the window and sade models
        xmlWindows = Utils.Config.getConfigurationFile("models.xml", "windows")
        xmlShades = Utils.Config.getConfigurationFile("models.xml", "shades")

        # for child in xmlWindows.iter("window"):
        for child in xmlWindows:
            insElement = CWindow()
            for attr in child:
                if attr.tag.strip().lower() == 'id':
                    insElement.ID = int(attr.text)
                if attr.tag.strip().lower() == 'name':
                    insElement.name = str(attr.text)
                if attr.tag.strip().lower() == 'aop':
                    insElement.aop = float(attr.text)
                if attr.tag.strip().lower() == 'bopout':
                    insElement.bopout = float(attr.text)
                if attr.tag.strip().lower() == 'shapeop':
                    insElement.shapeop = float(attr.text)
                if attr.tag.strip().lower() == 'a01arr':
                    insElement.a01arr = float(attr.text)
                if attr.tag.strip().lower() == 'b01inarr':
                    insElement.b01inarr = float(attr.text)
                if attr.tag.strip().lower() == 'b01outarr':
                    insElement.b01outarr = float(attr.text)
                if attr.tag.strip().lower() == 'b01absprevarr':
                    insElement.b01absprevarr = float(attr.text)
                if attr.tag.strip().lower() == 'b01rnarr':
                    insElement.b01rnarr = float(attr.text)
                if attr.tag.strip().lower() == 'a01int':
                    insElement.a01int = float(attr.text)
                if attr.tag.strip().lower() == 'b01inint':
                    insElement.b01inint = float(attr.text)
                if attr.tag.strip().lower() == 'b01outint':
                    insElement.b01outint = float(attr.text)
                if attr.tag.strip().lower() == 'b01presint':
                    insElement.b01presint = float(attr.text)
                if attr.tag.strip().lower() == 'b01rnint':
                    insElement.b01rnint = float(attr.text)
                if attr.tag.strip().lower() == 'a01dep':
                    insElement.a01dep = float(attr.text)
                if attr.tag.strip().lower() == 'b01outdep':
                    insElement.b01outdep = float(attr.text)
                if attr.tag.strip().lower() == 'b01absdep':
                    insElement.b01absdep = float(attr.text)
                if attr.tag.strip().lower() == 'b01gddep':
                    insElement.b01gddep = float(attr.text)
                if attr.tag.strip().lower() == 'a10dep':
                    insElement.a10dep = float(attr.text)
                if attr.tag.strip().lower() == 'b10indep':
                    insElement.b10indep = float(attr.text)
                if attr.tag.strip().lower() == 'b10outdep':
                    insElement.b10outdep = float(attr.text)
                if attr.tag.strip().lower() == 'b10absdep':
                    insElement.b10absdep = float(attr.text)
                if attr.tag.strip().lower() == 'b10gddep':
                    insElement.b10gddep = float(attr.text)

            self.pItems[insElement.UUID] = insElement
            # aggregate to the treeview
            self.tvwModels.insert(self.oWindows, "end", text=insElement.name, values=[typeOfClass.MODEL_WINDOW, insElement.UUID], tags=typeOfClass.MODEL_WINDOW, open=True)

        for child in xmlShades:
            insElement = CShade()
            for attr in child:
                if attr.tag.strip().lower() == 'id':
                    insElement.ID = int(attr.text)
                if attr.tag.strip().lower() == 'name':
                    insElement.name = str(attr.text)
                if attr.tag.strip().lower() == 'a01arr':
                    insElement.a01arr = float(attr.text)
                if attr.tag.strip().lower() == 'b01inarr':
                    insElement.b01inarr = float(attr.text)
                if attr.tag.strip().lower() == 'b01sarr':
                    insElement.b01sarr = float(attr.text)
                if attr.tag.strip().lower() == 'a10arr':
                    insElement.a10arr = float(attr.text)
                if attr.tag.strip().lower() == 'b10inarr':
                    insElement.b10inarr = float(attr.text)
                if attr.tag.strip().lower() == 'b10sarr':
                    insElement.b10sarr = float(attr.text)
                if attr.tag.strip().lower() == 'a01int':
                    insElement.a01int = float(attr.text)
                if attr.tag.strip().lower() == 'b01inint':
                    insElement.b01inint = float(attr.text)
                if attr.tag.strip().lower() == 'b01sint':
                    insElement.b01sint = float(attr.text)
                if attr.tag.strip().lower() == 'a10int':
                    insElement.a10int = float(attr.text)
                if attr.tag.strip().lower() == 'b10inint':
                    insElement.b10inint = float(attr.text)
                if attr.tag.strip().lower() == 'b10sint':
                    insElement.b10sint = float(attr.text)
                if attr.tag.strip().lower() == 'afullraise':
                    insElement.afullraise = float(attr.text)
                if attr.tag.strip().lower() == 'boutfullraise':
                    insElement.boutfullraise = float(attr.text)
                if attr.tag.strip().lower() == 'bsfullraise':
                    insElement.bsfullraise = float(attr.text)
                if attr.tag.strip().lower() == 'bsfulllower':
                    insElement.bsfulllower = float(attr.text)
                if attr.tag.strip().lower() == 'boutfulllower':
                    insElement.boutfulllower = float(attr.text)
                if attr.tag.strip().lower() == 'afulllower':
                    insElement.afulllower = float(attr.text)
                if attr.tag.strip().lower() == 'asflower':
                    insElement.aSFlower = float(attr.text)
                if attr.tag.strip().lower() == 'bsflower':
                    insElement.bSFlower = float(attr.text)
                if attr.tag.strip().lower() == 'shapelower':
                    insElement.shapelower = float(attr.text)

            self.pItems[insElement.UUID] = insElement
            # aggregate to the treeview
            self.tvwModels.insert(self.oShades, "end", text=insElement.name, values=[typeOfClass.MODEL_SHADE, insElement.UUID], tags=typeOfClass.MODEL_SHADE, open=True)

        return
    # end of loadModels
#
#
    def __init__(self, master):
        # app layout
        # +---------------------------------------------------
        # |  main menu
        # +---------------------------------------------------
        # |  main toolbar
        # +---------------------------------------------------
        # |  (Notebook)     |         (Notebook)
        # |                 |
        # |                 |
        # |                 |
        # |                 |
        # |  Bldgs | Models |  Sim | Edit | Log | Plots
        # +-----------------+---------------------------------
        # |  status bar
        # +---------------------------------------------------

        # create variables, objects
        self.simulation = Simulation()
        self.pItems = {}

        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.exitCallback)

        # initial setup of the main window
        self.master.resizable(False, False)
        self.master.minsize(320,240)
        self.master.geometry(Utils.Config.getDefaultWindowSize())
        self.master.title(Utils.Config.getWindowTitle())

        # main menu
        self.master.config(menu=Utils.UI.createMainMenuBar(self.master, self.newProject, self.openProject, self.saveProject, self.exitCallback))

        # main toolbar
        self.mainToolbar = self.createMainToolbar(self.master)
        self.mainToolbar.pack(side='top', fill='x')

        # main statusbar
        self.statusBar = self.createStatusBar(self.master)
        self.statusBar.pack(side='bottom', fill='x')

        # see layout above
        # create left and right panels
        self.pnlNavigation = tk.Frame(self.master, width=200, bd=1, relief=tk.SUNKEN)
        self.rightPanel = tk.Frame(self.master, width=640-(200), bd=1, relief=tk.SUNKEN)
        self.pnlNavigation.pack(side=tk.LEFT, fill=tk.Y) #expand=True
        self.rightPanel.pack(side='left', anchor='w', fill='both', expand=True)

        # create Buildings and Models treeview objects
        cssLeftTB = ttk.Style(self.master)
        cssLeftTB.configure('TNotebook', tabposition='sw')
        self.nbNavigation = ttk.Notebook(self.pnlNavigation, style='lefttab.TNotebook')
        self.frmBuildings = tk.Frame(self.nbNavigation, width=200)
        self.frmModels = tk.Frame(self.nbNavigation, width=200)
        self.nbNavigation.add(self.frmBuildings, text='Buildings')
        self.nbNavigation.add(self.frmModels, text='Models')
        self.nbNavigation.pack(pady=5, padx=5, anchor='nw', fill='both', expand=True, side='left')

        # contextual menu to configure items
        self.cmenuBuildings = tk.Menu(self.master, tearoff=0)
        self.cmenuBuildings.add_command(label="Rename", command = self.tvwBuildings_OnRenameItem)
        self.cmenuBuildings.add_separator()
        self.cmenuBuildings.add_command(label="Delete", command = self.tvwBuildings_OnDeleteItem)

        # treeview Buildings
        self.tvwBuildings = Utils.UI.Controls.ScrolledTreeView(self.frmBuildings, show="tree")
        self.tvwBuildings.column("#0",minwidth=250, stretch=True)
        self.tvwBuildings.bind("<<TreeviewSelect>>", lambda event, treeview=self.tvwBuildings:self.TreeView_OnNodeSelect(event, treeview))
        self.tvwBuildings.bind("<Delete>", self.tvwBuildings_OnDeleteItem)
        self.tvwBuildings.bind("<Double-1>", self.tvwBuildings_OnDoubleClickItem)
        if Utils.IO.isMacOS:
            self.tvwBuildings.bind("<Button-2>", self.tvwBuildings_OnContextMenu)
        if Utils.IO.isWindows or Utils.IO.isLinux:
            self.tvwBuildings.bind("<Button-3>", self.tvwBuildings_OnContextMenu)
        self.tvwBuildings.pack(side='left', anchor='w', fill='both', expand=True)
        self.tvwBuildings.focus()

        # treeview Models (NoMASS)
        self.tvwModels = Utils.UI.Controls.ScrolledTreeView(self.frmModels, show="tree")
        self.tvwModels.bind("<<TreeviewSelect>>", lambda event, treeview=self.tvwModels:self.TreeView_OnNodeSelect(event, treeview))
        self.tvwModels.pack(side='left', anchor='w', fill='both', expand=True)
        self.tvwModels.focus()

        # main panel where all data is displayed
        cssMainTB = ttk.Style(self.master)
        cssMainTB.configure('TNotebook', tabposition='sw')
        self.nbMain = ttk.Notebook(self.rightPanel, style='lefttab.TNotebook')
        self.tabConfiguration = Utils.UI.Controls.ScrollableContainer(self.nbMain, borderwidth=1, relief='groove', anchor='nw')
        self.tabEdit = Utils.UI.Controls.ScrollableContainer(self.nbMain, borderwidth=1, relief='groove', anchor='nw')
        self.tabRun = Utils.UI.Controls.ScrollableContainer(self.nbMain, borderwidth=1, relief='groove', anchor='nw')
        self.tabLog = tk.Frame(self.nbMain)
        self.tabLog.grid_rowconfigure(0, weight=1)
        self.tabLog.grid_columnconfigure(0, weight=1)
        self.tabPlots = Utils.UI.Controls.ScrollableContainer(self.nbMain, borderwidth=1, relief='groove', anchor='nw')

        self.nbMain.add(self.tabConfiguration, text='Configuration')
        self.nbMain.add(self.tabEdit, text='Edit')
        self.nbMain.add(self.tabRun, text='Run')
        self.nbMain.add(self.tabLog, text='Log')
        self.nbMain.add(self.tabPlots, text='Plots')
        self.nbMain.pack(pady=5, padx=5, anchor='nw', fill='both', expand=True, side='left')

        self.appCurrentState = typeOfAppStatus.IDLE

        self.createForms()
        self.initTabEdit()
        self.initBuilding()
        self.loadModels()

        self.fEmpty.title=""
        self.fEmpty.show()
        self.refreshTabEdit()

        self.sbmessage("Started!")
        self.nbMain.select(self.tabConfiguration)
        return
    # end of __init__

def refreshTabEdit(newHeight=None):
    app.refreshTabEdit(newHeight)

def updateProgressBar(value):
    app.updateProgressBar(value)

def sbmessage(message):
    app.sbmessage(message)

def log(message):
    app.log(message)

def appState(value=None):
    return app.appState(value)

def configuration():
    return app.simulation

def getListOfItemsByType(typeOfClass):
    return app.getListOfItemsByType(typeOfClass)

def getItemByType(typeOfClass):
    return app.getItemByType(typeOfClass)

def getListOfZones():
    return app.getListOfZones()
    

root = tk.Tk()
app = App(root)
uWin_Width = root.winfo_reqwidth()
uWin_Height = root.winfo_reqheight()
uLeft = int(root.winfo_screenwidth()/2 - uWin_Width/2) - 140
uTop = int(root.winfo_screenheight()/(2.5) - uWin_Height/2)
root.geometry("+{}+{}".format(uLeft, uTop))
root.mainloop()
