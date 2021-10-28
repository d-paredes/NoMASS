import uuid
import os
import sys
if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Enums"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Classes"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Utils"))
from CEnums import *
from COccupant import *
from COccupantTemplate import *
from CUtils import *

class FrmOccupantTemplates(object):
    @property
    def ID(self):
        return self._uuid

    @property
    def error(self):
        return self._error

    @property
    def message(self):
        return self._message

    @property
    def template(self):
        return self._template

    def clearOccupantsTab(self):
        for i in range(len(self._template._occupants)):
            del self._template._occupants[0]

        for widget in self.tabOccupants.interior.winfo_children():
            widget.destroy()

    def loadEmptyTemplate(self):
        self.txtName.configure(state="normal")
        self.txtDescription.configure(state="normal")
        self.ddlSector.configure(state="normal")
        self.ddlRegion.configure(state="normal")
        self.ddlCategory.configure(state="normal")

        self._template.UUID = Utils.Constants.emptyGUID
        self._template.ID = -1
        self._template.name = ""
        self._template.description = ""
        self._template.categoryID = "0"
        self._template.category = self._categories["0"]
        self._template.regionID = "0"
        self._template.region = self._regions["0"]
        self._template.sectorID = "0"
        self._template.sector = self._sectors["0"]

        self.ddlCategory.set(self._template.category)
        self.ddlRegion.set(self._template.region)
        self.ddlSector.set(self._template.sector)

        self.txtName.configure(state="readonly")
        self.txtDescription.configure(state="readonly")
        self.ddlSector.configure(state="disabled")
        self.ddlRegion.configure(state="disabled")
        self.ddlCategory.configure(state="disabled")

        self.tabGeneral.open()
        self.tabOccupants.close()

        # remove occupants
        self.clearOccupantsTab()
        return

    def tvwTemplates_OnNodeExpand(self, event):
        if self.tvwTemplates.selection() == None or self.tvwTemplates.selection() == "":
            return
        node = self.tvwTemplates.selection()[0]
        if len(self.tvwTemplates.get_children(node)) > 0:
            self.tvwTemplates.item(node, image=self._iconOpen)
        return

    def tvwTemplates_OnNodeCollapse(self, event):
        if self.tvwTemplates.selection() == None or self.tvwTemplates.selection() == "":
            return
        node = self.tvwTemplates.selection()[0]
        if len(self.tvwTemplates.get_children(node)) > 0:
            self.tvwTemplates.item(node, image=self._iconClose)
        return

    def tvwTemplates_OnNodeSelect(self, event):
        if self.tvwTemplates.selection() == None or self.tvwTemplates.selection() == "":
            return
        node = self.tvwTemplates.selection()[0]
        typeOfObject = self.tvwTemplates.item(node)["values"][0]
        key = self.tvwTemplates.item(node)["values"][1]

        # load empty template when selecting a folder node
        if str(typeOfObject).strip().lower() == "__category__":
            self.loadEmptyTemplate()
            return

        # display the selected template
        _template = self.getTemplate(key)
        if _template is None:
            return

        # remove occupants
        self.clearOccupantsTab()

        self.txtName.configure(state="normal")
        self.txtDescription.configure(state="normal")
        self.ddlSector.configure(state="normal")
        self.ddlRegion.configure(state="normal")
        self.ddlCategory.configure(state="normal")

        self._template.UUID = _template.UUID
        self._template.ID = _template.ID
        self._template.name = _template.name
        self._template.description = _template.description
        #print(self._categories)
        self._template.categoryID = _template.categoryID
        self._template.category = self._categories[_template.categoryID]
        self._template.regionID = _template.regionID
        self._template.region = self._regions[_template.regionID]
        self._template.sectorID = _template.sectorID
        self._template.sector = self._sectors[_template.sectorID]

        self.ddlCategory.set(self._template.category)
        self.ddlRegion.set(self._template.region)
        self.ddlSector.set(self._template.sector)

        for occupant in _template.occupants:
            self._template.occupants.append(occupant)

        # display occupants belonging to the selected template
        containerTemp = tk.Frame(self.tabOccupants.interior)
        lbl = tk.Label(containerTemp, text="Number of Occupants:", width=20, anchor='w')
        lbl.pack(side="left", padx=5)
        lbl = tk.Label(containerTemp, text=str(len(self._template.occupants)), width=14, anchor='e')
        lbl.pack(fill="x", expand=True, side="right", padx=5)
        containerTemp.pack(fill="x", pady=(5,0))

        i=0
        for occupant in self._template.occupants:
            newTab = Utils.UI.Controls.CollapsibleFrame(self.tabOccupants.interior, text ="Occupant " + str(i), interior_padx=6, icon_open=Utils.Resources.Icons.plus_9_0_333333, icon_close=Utils.Resources.Icons.minus_9_0_333333)

            containerTemp = tk.Frame(newTab.interior)
            lbl = tk.Label(containerTemp, text="Zone", width=10, anchor='w')
            lbl.pack(side="left", padx=5)
            ddlValue = Utils.UI.Controls.CascadingDropDownList(containerTemp, linkedID=None, textvariable=occupant._zoneId, kvData=self._zones, catalogName="", loadFromFile=False, defaultValue=None, state="readonly", exportselection=0)
            ddlValue.pack(fill="x", padx=5, expand=True)
            containerTemp.pack(fill="x", pady=(2,0))

            containerTemp = tk.Frame(newTab.interior)
            lbl = tk.Label(containerTemp, text="Power", width=10, anchor='w')
            lbl.pack(side="left", padx=5)
            txtValue = tk.Spinbox(containerTemp, from_=0.0, to=1.0, increment=0.05, state='readonly', textvariable=occupant._power)
            txtValue.pack(fill="x", padx=5, expand=True)
            containerTemp.pack(fill="x", pady=(2,0))

            containerTemp = tk.Frame(newTab.interior)
            lbl = tk.Label(containerTemp, text="Window ID", width=10, anchor='w')
            lbl.pack(side="left", padx=5)
            ddlValue = Utils.UI.Controls.CascadingDropDownList(containerTemp, linkedID=None, textvariable=occupant._windowId, kvData=Utils.Config.getCatalog("windows"), catalogName="", loadFromFile=False, defaultValue=occupant.windowId, state="readonly", exportselection=0)
            ddlValue.configure(state='disabled')
            ddlValue.pack(fill="x", padx=5, expand=True)
            containerTemp.pack(fill="x", pady=(2,0))

            containerTemp = tk.Frame(newTab.interior)
            lbl = tk.Label(containerTemp, text="Shade ID", width=10, anchor='w')
            lbl.pack(side="left", padx=5)
            ddlValue = Utils.UI.Controls.CascadingDropDownList(containerTemp, linkedID=None, textvariable=occupant._shadeId, kvData=Utils.Config.getCatalog("shades"), catalogName="", loadFromFile=False, defaultValue=occupant.shadeId, state="readonly", exportselection=0)
            ddlValue.configure(state='disabled')
            ddlValue.pack(fill="x", padx=5, expand=True)
            containerTemp.pack(fill="x", pady=(2,0))

            containerTemp = tk.Frame(newTab.interior)
            lbl = tk.Label(containerTemp, text="Activity ID", width=10, anchor='w')
            lbl.pack(side="left", padx=5)
            ddlValue = Utils.UI.Controls.CascadingDropDownList(containerTemp, linkedID=None, textvariable=occupant._activityId, kvData=Utils.Config.getCatalog("activity"), catalogName="", loadFromFile=False, defaultValue=occupant.activityId, state="readonly", exportselection=0)
            ddlValue.configure(state='disabled')
            ddlValue.pack(fill="x", padx=5, expand=True)
            containerTemp.pack(fill="x", pady=(2,0))

            containerTemp = tk.Frame(newTab.interior)
            lbl = tk.Label(containerTemp, text="Gender", width=10, anchor='w')
            lbl.pack(side="left", padx=5)
            ddlValue = Utils.UI.Controls.CascadingDropDownList(containerTemp, linkedID=None, textvariable=occupant._sex, kvData=Utils.Config.getCatalog("sex"), catalogName="", loadFromFile=False, defaultValue=occupant.sex, state="readonly", exportselection=0)
            ddlValue.configure(state='disabled')
            ddlValue.pack(fill="x", padx=5, expand=True)
            containerTemp.pack(fill="x", pady=(2,0))

            containerTemp = tk.Frame(newTab.interior)
            lbl = tk.Label(containerTemp, text="Family", width=10, anchor='w')
            lbl.pack(side="left", padx=5)
            ddlValue = Utils.UI.Controls.CascadingDropDownList(containerTemp, linkedID=None, textvariable=occupant._familyID, kvData=Utils.Config.getCatalog("family"), catalogName="", loadFromFile=False, defaultValue=occupant.familyID, state="readonly", exportselection=0)
            ddlValue.configure(state='disabled')
            ddlValue.pack(fill="x", padx=5, expand=True)
            containerTemp.pack(fill="x", pady=(2,0))

            containerTemp = tk.Frame(newTab.interior)
            lbl = tk.Label(containerTemp, text="Education", width=10, anchor='w')
            lbl.pack(side="left", padx=5)
            ddlValue = Utils.UI.Controls.CascadingDropDownList(containerTemp, linkedID=None, textvariable=occupant._educationID, kvData=Utils.Config.getCatalog("education"), catalogName="", loadFromFile=False, defaultValue=occupant.educationID, state="readonly", exportselection=0)
            ddlValue.configure(state='disabled')
            ddlValue.pack(fill="x", padx=5, expand=True)
            containerTemp.pack(fill="x", pady=(2,0))

            containerTemp = tk.Frame(newTab.interior)
            lbl = tk.Label(containerTemp, text="Age", width=10, anchor='w')
            lbl.pack(side="left", padx=5)
            ddlValue = Utils.UI.Controls.CascadingDropDownList(containerTemp, linkedID=None, textvariable=occupant._ageID, kvData=Utils.Config.getCatalog("age"), catalogName="", loadFromFile=False, defaultValue=occupant.ageGroup, state="readonly", exportselection=0)
            ddlValue.configure(state='disabled')
            ddlValue.pack(fill="x", padx=5, expand=True)
            containerTemp.pack(fill="x", pady=(2,0))

            containerTemp = tk.Frame(newTab.interior)
            chk = tk.Checkbutton(containerTemp, text="Own computer", anchor='w', onvalue=True, offvalue=False, variable=occupant._ownComputer)
            chk.configure(state='disabled')
            chk.pack(fill='x', side="left", padx=5)
            containerTemp.pack(fill="x", pady=(2,0))

            containerTemp = tk.Frame(newTab.interior)
            chk = tk.Checkbutton(containerTemp, text="Is retired", anchor='w', onvalue=True, offvalue=False, variable=occupant._isRetired)
            chk.configure(state='disabled')
            chk.pack(fill='x', side="left", padx=5)
            containerTemp.pack(fill="x", pady=(2,0))

            containerTemp = tk.Frame(newTab.interior)
            chk = tk.Checkbutton(containerTemp, text="Is married", anchor='w', onvalue=True, offvalue=False, variable=occupant._isMarried)
            chk.configure(state='disabled')
            chk.pack(fill='x', side="left", padx=5)
            containerTemp.pack(fill="x", pady=(2,0))

            containerTemp = tk.Frame(newTab.interior)
            chk = tk.Checkbutton(containerTemp, text="Is unemployed", anchor='w', onvalue=True, offvalue=False, variable=occupant._isUnEmployed)
            chk.configure(state='disabled')
            chk.pack(fill='x', side="left", padx=5)
            containerTemp.pack(fill="x", pady=(2,0))

            newTab.pack(fill="x", pady=(5,(0 if i < len(self._template.occupants)-1 else 10)))
            newTab.open()
            i += 1

        self.txtName.configure(state="readonly")
        self.txtDescription.configure(state="readonly")
        self.ddlSector.configure(state="disabled")
        self.ddlRegion.configure(state="disabled")
        self.ddlCategory.configure(state="disabled")

        self.tabGeneral.open()

        self.dataContainer.update()
        self.dataContainer.updateViewPort(self.dataContainer.width, 250+(300*len(self._template.occupants))+(30 if len(self._template.occupants) > 0 else 0))

        return

    # other callbacks
    def OnCancel(self, event=None):
        if messagebox.askokcancel("Quit", "Do you really wish to cancel?"):
            self._error = False
            self._message = ""
            self._template.UUID = Utils.Constants.emptyGUID
            self.top.destroy()

    def loadTemplatesFromFile(self):
        # load list of categories
        xmlCategories = Utils.Config.getConfigurationFile("occupantTemplates.xml", "categories")
        xmlTemplates = Utils.Config.getConfigurationFile("occupantTemplates.xml", "templates")
        templates = []

        # remove items from treeview
        self.tvwTemplates.delete(*self.tvwTemplates.get_children())

        for category in xmlCategories:
            id = category.find("id").text.strip()
            newNodeCategory = self.tvwTemplates.insert("", tk.END, text=category.find("name").text.strip(), values=("__category__", id), tags="__category__", open=True, image=self._iconOpen)
            for template in xmlTemplates.iter("template"):
                if template.find("typeID").text.strip().lower() == str(id).strip().lower():
                    newOccupantTemplate = COccupantTemplate(
                        id=template.find("id").text,
                        name=template.find("name").text,
                        description=template.find('description').text,
                        categoryID=template.find('categoryID').text,
                        category="",
                        regionID=template.find('regionID').text,
                        region="",
                        sectorID=template.find('sectorID').text,
                        sector="")
                    for occupant in template.find("occupants"):
                        newOccupant = COccupant(
                            id=int(occupant.find('id').text),
                            name="Undefined",
                            zoneId=occupant.find('zoneId').text,
                            zone=occupant.find('zoneId').text,
                            power=float(occupant.find('power').text),
                            windowId=occupant.find('windowId').text,
                            window=occupant.find('window').text,
                            shadeId=occupant.find('shadeId').text,
                            shade=occupant.find('shade').text,
                            activityId=occupant.find('activityId').text,
                            sex=occupant.find('sex').text,
                            familyID=occupant.find('familyID').text,
                            educationID=occupant.find('educationID').text,
                            ageGroup=occupant.find('ageGroup').text,
                            ownComputer=bool(int(occupant.find('ownComputer').text)==1),
                            isRetired=bool(int(occupant.find('isRetired').text)==1),
                            isMarried=bool(int(occupant.find('isMarried').text)==1),
                            isUnEmployed=bool(int(occupant.find('isUnEmployed').text)==1)
                        )
                        newOccupantTemplate.occupants.append(newOccupant)

                    templates.append(newOccupantTemplate)
                    newNodeTemplate = self.tvwTemplates.insert(newNodeCategory, tk.END, text=newOccupantTemplate.name, values=("__template__", newOccupantTemplate.UUID), tags="__template__", open=True, image=self._iconTemplate)
        return templates

    def getTemplate(self, templateID):
        try:
            self._occupantTemplates
        except NameError:
            return None

        for item in self._occupantTemplates:
            if item.UUID == templateID:
                return item
        return None

    def txtPower_OnPowerChanged(self, sender):
        sumPower = 0
        for occupant in self._template.occupants:
                sumPower += occupant.power.get()

    def btnOK_OnClick(self):
        if self._template.UUID == Utils.Constants.emptyGUID:
            messagebox.showerror(title='Error!', message="Select a valid template from the list")
            return

        if len(self._template.occupants) == 0:
            messagebox.showerror(title='Error!', message="Select a valid template from the list")
            return

        self._error = False
        self._message = ""

        self.top.destroy()

    def __init__(self, top, pZones, value = None):
        self._uuid = str(uuid.uuid4())
        ## colours, icons
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#d9d9d9' # X11 color: 'gray85'
        _width = 275
        _height = 510
        self._iconOpen = tk.PhotoImage(data=Utils.Resources.Icons.folder_open_o_16_0_d4be2b)
        self._iconClose = tk.PhotoImage(data=Utils.Resources.Icons.folder_o_16_0_d4be2b)
        self._iconTemplate = tk.PhotoImage(data=Utils.Resources.Icons.child_16_0_00aa00)

        self.top = tk.Toplevel(top)
        self.top.transient(top)
        self.top.grab_set()
        uX = (top.winfo_screenwidth() - top.winfo_reqwidth()) / 2
        uY = (top.winfo_screenheight() - top.winfo_reqheight()) / 2
        self.top.geometry("%dx%d+%d+%d" % (_width, _height, uX, uY))

        self.top.title("Select occupant template")

        # no resize window and OnClose event
        self.top.resizable(False, False)
        self.top.protocol("WM_DELETE_WINDOW", self.OnCancel)

        # variables
        self._error = False
        self._message = ""
        self._zones = {}
        for zone in pZones:
            self._zones[zone.UUID] = zone.name
        self._template = COccupantTemplate()

        # create treeview to displate all the templates
        self.tvwTemplates = Utils.UI.Controls.ScrolledTreeView(self.top, show="tree")
        self.tvwTemplates.bind("<<TreeviewSelect>>", self.tvwTemplates_OnNodeSelect)
        self.tvwTemplates.bind("<<TreeviewOpen>>", self.tvwTemplates_OnNodeExpand)
        self.tvwTemplates.bind("<<TreeviewClose>>", self.tvwTemplates_OnNodeCollapse)
        self.tvwTemplates.bind("<Escape>", self.OnCancel)
        self.tvwTemplates.place(relx=0.0, rely=0.0, relheight=0.4, relwidth=1.0)

        # load data options from file
        self._occupantTemplates = self.loadTemplatesFromFile()
        self._categories = Utils.Config.getCatalog("categories")
        self._regions = Utils.Config.getCatalog("regions")
        self._sectors = Utils.Config.getCatalog("sectors")

        # action buttons
        self.btnCancel = ttk.Button(self.top, command=self.OnCancel)
        self.btnCancel.place(relx=0.125, rely=0.93, height=25, width=76)
        self.btnCancel.configure(takefocus="")
        self.btnCancel.configure(text="Cancel")

        self.btnOK = ttk.Button(self.top, command=self.btnOK_OnClick)
        self.btnOK.place(relx=0.5, rely=0.93, height=25, width=76)
        self.btnOK.configure(takefocus="")
        self.btnOK.configure(text="OK")

        # lower frame to display data
        self.dataContainer = Utils.UI.Controls.ScrollableContainer(self.top, borderwidth=1, relief='groove')
        self.dataContainer.place(relx=0.0, rely=0.43, relheight=0.48, relwidth=1)

        # tabs
        self.tabGeneral = Utils.UI.Controls.CollapsibleFrame(self.dataContainer.innerframe, text ="General", interior_padx=6, icon_open=Utils.Resources.Icons.angle_down_16_0_333333, icon_close=Utils.Resources.Icons.angle_up_16_0_333333)
        self.tabGeneral.pack(fill="x")
        self.tabOccupants = Utils.UI.Controls.CollapsibleFrame(self.dataContainer.innerframe, text ="Occupants", interior_padx=6, icon_open=Utils.Resources.Icons.angle_down_16_0_333333, icon_close=Utils.Resources.Icons.angle_up_16_0_333333)#, background="#00ffaa")
        self.tabOccupants.pack(fill="x")

        # 'General' tab
        containerTemp = tk.Frame(self.tabGeneral.interior)
        lbl = tk.Label(containerTemp, text="Name", width=10, anchor='w')
        lbl.pack(side="left", padx=5, pady=2)
        self.txtName = tk.Entry(containerTemp, textvariable=self._template._name)
        self.txtName.pack(fill="x", padx=5, expand=True)
        containerTemp.pack(fill="x")

        containerTemp = tk.Frame(self.tabGeneral.interior)
        lbl = tk.Label(containerTemp, text="Description", width=10, anchor='w')
        lbl.pack(side="left", padx=5, pady=2)
        self.txtDescription = tk.Entry(containerTemp, textvariable=self._template._description)
        self.txtDescription.pack(fill="x", padx=5, expand=True)
        containerTemp.pack(fill="x")

        # cascading drop down lists
        containerSector = tk.Frame(self.tabGeneral.interior)
        lbl = tk.Label(containerSector, text="Sector", width=10, anchor='w')
        lbl.pack(side="left", padx=5, pady=2)
        self.ddlSector = Utils.UI.Controls.CascadingDropDownList(containerSector, linkedID=None, textvariable=self._template._sectorID, kvData={}, catalogName="sectors", loadFromFile=True, defaultValue=None, state="readonly", exportselection=0)
        self.ddlSector.pack(fill="x", padx=5, expand=True)

        # cascading drop down lists
        containerRegion = tk.Frame(self.tabGeneral.interior)
        lbl = tk.Label(containerRegion, text="Region", width=10, anchor='w')
        lbl.pack(side="left", padx=5, pady=2)
        self.ddlRegion = Utils.UI.Controls.CascadingDropDownList(containerRegion, linkedID=self.ddlSector, textvariable=self._template._regionID, kvData={}, catalogName="regions", loadFromFile=True, defaultValue=None, state="readonly", exportselection=0)
        self.ddlRegion.pack(fill="x", padx=5, expand=True)

        # cascading drop down lists
        containerCategory = tk.Frame(self.tabGeneral.interior)
        lbl = tk.Label(containerCategory, text="Category", width=10, anchor='w')
        lbl.pack(side="left", padx=5, pady=2)
        self.ddlCategory = Utils.UI.Controls.CascadingDropDownList(containerCategory, linkedID=self.ddlRegion, textvariable=self._template._categoryID, kvData={}, catalogName="categories", loadFromFile=True, defaultValue=None, state="readonly", exportselection=0)
        self.ddlCategory.pack(fill="x", padx=5, expand=True)

        containerCategory.pack(fill="x")
        containerRegion.pack(fill="x")
        containerSector.pack(fill="x")

        # select the first item in the tree
        _initNode = self.tvwTemplates.get_children()[0]
        self.tvwTemplates.selection_set(_initNode)
        self.tvwTemplates.focus_set()
        self.tvwTemplates.focus(_initNode)

        # refresh the lower frame container to set scrollbars
        self.dataContainer.update()
        self.dataContainer.updateViewPort(self.dataContainer.width, 1200)
        return
# end of FrmOccupantTemplates