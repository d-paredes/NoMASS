import uuid
import os
import sys
if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Enums"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Utils"))
from CEnums import *
from CUtils import *

class FrmOccupant(object):
    def load(self, id=None, name=None, description=None, categoryID=None, category=None, regionID=None, region=None, sectorID=None, sector=None, occupants=None, zones=None, show=False, enabled=False):
        if id is not None:
            self._id = id

        if name is not None:
            self._name = name
            self.txtname.config(textvariable=self._name, state="disabled")

        if description is not None:
            self._description = description
            self.txtdescription.config(textvariable=self._description, state="disabled")

        if sectorID is not None:
            self._sectorID = sectorID

        if sector is not None:
            self._sector = sector
            self.ddlSector.config(state="disabled")
            self.ddlSector.setVariable(self._sector)
            self.ddlSector.config(state="disabled")

        if regionID is not None:
            self._regionID = regionID

        if region is not None:
            self._region = region
            self.ddlRegion.config(state="disabled")
            self.ddlRegion.setVariable(self._region)
            self.ddlRegion.config(state="disabled")

        if categoryID is not None:
            self._categoryID = categoryID

        if category is not None:
            self._category = category
            # print("         _category  >> ", self._category.get())
            self.ddlCategory.config(state="disabled")
            self.ddlCategory.setVariable(self._category)
            self.ddlCategory.config(state="disabled")

        if occupants is None or len(occupants) != 1:
            return

        _occupant = occupants[0]

        self._zones = collections.OrderedDict(sorted(zones.copy().items(), key=lambda x: x[1]))
        self.ddlZone._kvData=self._zones
        self.ddlZone.configure(values=self.ddlZone._kvData.values())

        if _occupant.zoneId is not None:
            self._zoneId = occupants[0]._zoneId
            self._zone = occupants[0]._zone
            self.ddlZone.setVariable(self._zoneId)

        if _occupant.power is not None:
            self._power = occupants[0]._power
            self.txtPower.config(textvariable=self._power, state="normal")

        if _occupant.windowId is not None:
            self._windowId = occupants[0]._windowId
            self._window = occupants[0]._window
            self.ddlWindow.setVariables(self._windowId, self._window)

        if _occupant.shadeId is not None:
            self._shadeId = occupants[0]._shadeId
            self._shade = occupants[0]._shade
            self.ddlShade.setVariables(self._shadeId, self._shade)

        if _occupant.activityId is not None:
            self._activityId = occupants[0]._activityId

        if _occupant.sex is not None:
            self._sexID = occupants[0]._sex
            self.ddlGender.setVariable(self._sexID)

        if _occupant.familyID is not None:
            self._familyID = occupants[0]._familyID
            self.ddlFamily.setVariable(self._familyID)

        if _occupant.educationID is not None:
            self._educationID = occupants[0]._educationID
            self.ddlEducation.setVariable(self._educationID)

        if _occupant.ageGroup is not None:
            self._ageID = occupants[0]._ageID
            self.ddlAge.setVariable(self._ageID)

        if _occupant.ownComputer is not None:
            self._ownComputer = occupants[0]._ownComputer
            self.chkOwnComputer.config(variable=self._ownComputer)

        if _occupant.isRetired is not None:
            self._isRetired = occupants[0]._isRetired
            self.chkIsRetired.config(variable=self._isRetired)

        if _occupant.isMarried is not None:
            self._isMarried = occupants[0]._isMarried
            self.chkIsMarried.config(variable=self._isMarried)

        if _occupant.isUnEmployed is not None:
            self._isUnEmployed = occupants[0]._isUnEmployed
            self.chkIsEmployed.config(variable=self._isUnEmployed)

        if show:
            self._parentWidget.refreshTabEdit(500)
            self.show()

    def updateZoneList(self, zones):
        self._zones = collections.OrderedDict(sorted(zones.copy().items(), key=lambda x: x[1]))
        self.ddlZone._kvData=self._zones

    def show(self):
        self._frame.tkraise()

    def __init__(self, master, parent, uuid=str(uuid.uuid4()), id=0, name='', description='', categoryID='', category='', regionID='', region='', sectorID='', sector='', power=0, zoneId='', occupants=None, zones={"undefined":"undefinded"}):
        form_margin_top = 10
        column_width = 25
        padding_outer = 100
        padding_inner = 5
        padding_top = 2
        padding_btm = 2

        self._parentWidget = master

        self._uuid = uuid

        self._typeOfClass = tk.IntVar()
        self._id = tk.IntVar()
        self._name = tk.StringVar()
        self._description = tk.StringVar()
        self._categoryID = tk.StringVar()
        self._category = tk.StringVar()
        self._regionID = tk.StringVar()
        self._region = tk.StringVar()
        self._sectorID = tk.StringVar()
        self._sector = tk.StringVar()
        self._zones = zones

        self._zoneId = tk.StringVar()
        self._zone = tk.StringVar()
        self._power = tk.DoubleVar()
        self._windowId = tk.StringVar()
        self._window = tk.StringVar()
        self._shadeId = tk.StringVar()
        self._shade = tk.StringVar()
        self._activityId = tk.StringVar()
        self._sexID = tk.StringVar()
        self._familyID = tk.StringVar()
        self._educationID = tk.StringVar()
        self._ageID = tk.StringVar()
        self._ownComputer = tk.BooleanVar()
        self._isRetired = tk.BooleanVar()
        self._isMarried = tk.BooleanVar()
        self._isUnEmployed = tk.BooleanVar()

        self._typeOfClass = typeOfClass.BUILDING_OCCUPANT
        self._frame = tk.Frame(parent, width=parent.winfo_reqwidth(), height=parent.winfo_reqheight())
        self._frame.grid(row=0, column=0, sticky="nsew")

        self.tabGeneral = Utils.UI.Controls.CollapsibleFrame(self._frame, text ="General", interior_padx=6, icon_open=Utils.Resources.Icons.angle_down_16_0_333333, icon_close=Utils.Resources.Icons.angle_up_16_0_333333)#, background="#00ff00")
        self.tabGeneral.pack(fill=tk.X)
        self.tabOccupant = Utils.UI.Controls.CollapsibleFrame(self._frame, text ="Occupant", interior_padx=6, icon_open=Utils.Resources.Icons.angle_down_16_0_333333, icon_close=Utils.Resources.Icons.angle_up_16_0_333333)#, background="#00ff22")
        self.tabOccupant.pack(fill=tk.X)

        containerTemp = tk.Frame(self.tabGeneral.interior)
        self.lblname = tk.Label(containerTemp, text="Name:", width=column_width, anchor="w")
        self.lblname.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtname = tk.Entry(containerTemp, justify="right")
        self.txtname.config(textvariable=self._name, state="disabled")
        self.txtname.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=(padding_outer, int(padding_outer / 2)), pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self.tabGeneral.interior)
        self.lbldescription = tk.Label(containerTemp, text="Description:", width=column_width, anchor="w")
        self.lbldescription.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtdescription = tk.Entry(containerTemp, justify="right")
        self.txtdescription.config(textvariable=self._description, state="disabled")
        self.txtdescription.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=(padding_outer, int(padding_outer / 2)), pady=(padding_top, 0))

        containerSector = tk.Frame(self.tabGeneral.interior)
        self.lblsector = tk.Label(containerSector, text="Sector:", width=column_width, anchor="w")
        self.lblsector.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.ddlSector = Utils.UI.Controls.DropDownList(containerSector, textvariable=self._sectorID, kvData=Utils.Config.getCatalog("sectors"), catalogName="sectors", initialValue=self._sectorID.get(), state="disabled", exportselection=0)
        self.ddlSector.pack(fill="x", expand=True, side="left")

        containerRegion = tk.Frame(self.tabGeneral.interior)
        self.lblregion = tk.Label(containerRegion, text="Region:", width=column_width, anchor="w")
        self.lblregion.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.ddlRegion = Utils.UI.Controls.DropDownList(containerRegion, textvariable=self._regionID, kvData=Utils.Config.getCatalog("regions"), nestedControlID=self.ddlSector, catalogName="regions", initialValue=self._regionID.get(), state="disabled", exportselection=0)
        self.ddlRegion.pack(fill="x", expand=True, side="left")

        containerCategory = tk.Frame(self.tabGeneral.interior)
        self.lblcategory = tk.Label(containerCategory, text="Category:", width=column_width, anchor="w")
        self.lblcategory.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.ddlCategory = Utils.UI.Controls.DropDownList(containerCategory, textvariable=self._categoryID, kvData=Utils.Config.getCatalog("categories"), catalogName="categories", nestedControlID=self.ddlRegion, initialValue=self._categoryID.get(), state="disabled", exportselection=0)
        self.ddlCategory.pack(fill="x", expand=True, side="left")

        containerCategory.pack(fill="x", padx=(padding_outer, int(padding_outer / 2)), pady=(padding_top, 0))
        containerRegion.pack(fill="x", padx=(padding_outer, int(padding_outer / 2)), pady=(padding_top, 0))
        containerSector.pack(fill="x", padx=(padding_outer, int(padding_outer / 2)), pady=(padding_top, 0))

        # --------------------------------------------------------------------------------
        # occupant detail

        containerTemp = tk.Frame(self.tabOccupant.interior)
        self.lblzone = tk.Label(containerTemp, text="Zone:", width=column_width, anchor="w")
        self.lblzone.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.ddlZone = Utils.UI.Controls.DropDownList(containerTemp, textvariable=self._zoneId, kvData=self._zones, initialValue=self._zoneId.get(), state="normal", exportselection=0)
        self.ddlZone.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=(padding_outer, int(padding_outer / 2)), pady=(padding_top, 0))

        containerTemp = tk.Frame(self.tabOccupant.interior)
        self.lblpower = tk.Label(containerTemp, text="Power:", width=column_width, anchor="w")
        self.lblpower.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtPower = tk.Spinbox(containerTemp, from_=0.0, to=1.0, increment=0.05, state="normal", textvariable=self._power)
        self.txtPower.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=(padding_outer, int(padding_outer / 2)), pady=(padding_top, 0))

        containerTemp = tk.Frame(self.tabOccupant.interior)
        self.lblwindowId = tk.Label(containerTemp, text="Window:", width=column_width, anchor="w")
        self.lblwindowId.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.ddlWindow = Utils.UI.Controls.DropDownList(containerTemp, textvariable=self._windowId, kvData=Utils.Config.getCatalog("windows"), initialValue=self._windowId.get(), state="normal", exportselection=0)
        self.ddlWindow.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=(padding_outer, int(padding_outer / 2)), pady=(padding_top, 0))

        containerTemp = tk.Frame(self.tabOccupant.interior)
        self.lblshadeId = tk.Label(containerTemp, text="Shade:", width=column_width, anchor="w")
        self.lblshadeId.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.ddlShade = Utils.UI.Controls.DropDownList(containerTemp, textvariable=self._shadeId, kvData=Utils.Config.getCatalog("shades"), initialValue=self._shadeId.get(), state="normal", exportselection=0)
        self.ddlShade.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=(padding_outer, int(padding_outer / 2)), pady=(padding_top, 0))

        containerTemp = tk.Frame(self.tabOccupant.interior)
        self.lblsex = tk.Label(containerTemp, text="Gender:", width=column_width, anchor="w")
        self.lblsex.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.ddlGender = Utils.UI.Controls.DropDownList(containerTemp, textvariable=self._sexID, kvData=Utils.Config.getCatalog("sex"), initialValue=self._sexID.get(), state="normal", exportselection=0)
        self.ddlGender.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=(padding_outer, int(padding_outer / 2)), pady=(padding_top, 0))

        containerTemp = tk.Frame(self.tabOccupant.interior)
        self.lblfamilyID = tk.Label(containerTemp, text="Family:", width=column_width, anchor="w")
        self.lblfamilyID.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.ddlFamily = Utils.UI.Controls.DropDownList(containerTemp, textvariable=self._familyID, kvData=Utils.Config.getCatalog("family"), initialValue=self._familyID.get(), state="normal", exportselection=0)
        self.ddlFamily.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=(padding_outer, int(padding_outer / 2)), pady=(padding_top, 0))

        containerTemp = tk.Frame(self.tabOccupant.interior)
        self.lbleducationID = tk.Label(containerTemp, text="Education:", width=column_width, anchor="w")
        self.lbleducationID.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.ddlEducation = Utils.UI.Controls.DropDownList(containerTemp, textvariable=self._educationID, kvData=Utils.Config.getCatalog("education"), initialValue=self._educationID.get(), state="normal", exportselection=0)
        self.ddlEducation.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=(padding_outer, int(padding_outer / 2)), pady=(padding_top, 0))

        containerTemp = tk.Frame(self.tabOccupant.interior)
        self.lblageID = tk.Label(containerTemp, text="Age:", width=column_width, anchor="w")
        self.lblageID.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.ddlAge = Utils.UI.Controls.DropDownList(containerTemp, textvariable=self._ageID, kvData=Utils.Config.getCatalog("age"), initialValue=self._ageID.get(), state="normal", exportselection=0)
        self.ddlAge.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=(padding_outer, int(padding_outer / 2)), pady=(padding_top, 0))

        containerTemp = tk.Frame(self.tabOccupant.interior)
        self.lblownComputer = tk.Label(containerTemp, text="Own computer:", width=column_width, anchor="w")
        self.lblownComputer.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.chkOwnComputer = tk.Checkbutton(containerTemp, text="", anchor='w', onvalue=True, offvalue=False, variable=self._ownComputer)
        self.chkOwnComputer.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=(padding_outer, int(padding_outer / 2)), pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self.tabOccupant.interior)
        self.lblisRetired = tk.Label(containerTemp, text="Is retired:", width=column_width, anchor="w")
        self.lblisRetired.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.chkIsRetired = tk.Checkbutton(containerTemp, text="", anchor='w', onvalue=True, offvalue=False, variable=self._isRetired)
        self.chkIsRetired.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=(padding_outer, int(padding_outer / 2)), pady=(padding_top, 0))

        containerTemp = tk.Frame(self.tabOccupant.interior)
        self.lblisMarried = tk.Label(containerTemp, text="Is married:", width=column_width, anchor="w")
        self.lblisMarried.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.chkIsMarried = tk.Checkbutton(containerTemp, text="", anchor='w', onvalue=True, offvalue=False, variable=self._isMarried)
        self.chkIsMarried.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=(padding_outer, int(padding_outer / 2)), pady=(padding_top, 0))

        containerTemp = tk.Frame(self.tabOccupant.interior)
        self.lblisUnEmployed = tk.Label(containerTemp, text="Is unemployed:", width=column_width, anchor="w")
        self.lblisUnEmployed.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.chkIsEmployed = tk.Checkbutton(containerTemp, text="", anchor='w', onvalue=True, offvalue=False, variable=self._isUnEmployed)
        self.chkIsEmployed.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=(padding_outer, int(padding_outer / 2)), pady=(padding_top, 0))

        self._id.set(id)
        self._name.set(name)
        self._description.set(description)

        self.tabGeneral.open()
        self.tabOccupant.open()
        self._frame.update_idletasks()
        return
# end of FrmOccupant