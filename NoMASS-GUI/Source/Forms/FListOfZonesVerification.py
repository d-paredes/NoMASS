import uuid
import os
import sys
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

class FrmListOfZonesVerification(object):
    @property
    def ID(self):
        return self._uuid

    @property
    def error(self):
        return self._error

    @property
    def confirm(self):
        return self._confirm

    @property
    def message(self):
        return self._message

    # other callbacks
    def OnCancel(self, event=None):
        if messagebox.askokcancel("Quit", "Do you really wish to cancel?"):
            self._error = False
            self._message = ""
            self._confirm = False
            self.top.destroy()

    def btnOK_OnClick(self):
        if messagebox.askokcancel("Confirm", "Are you sure zones in the idf file match the list of zones in the configuration?"):
            self._error = False
            self._message = ""
            self._confirm = True
            self.top.destroy()

    def compareLists(self):
        if len(self._zonesIDF) != len(self._zonesGUI):
            self._error = True
            self._message = "Number of zones does not match the listed zones in the IDF file"
            self._confirm = False
            self.lblMessage.configure(text=self._message)
            self.btnOK.configure(state="normal")
            return False

        for _zoneIDF in self._zonesIDF:
            if _zoneIDF not in self._zonesGUI:
                self._error = True
                self._message = ("Zone %s not found in the configuration" % (_zoneIDF))
                self._confirm = False
                self.lblMessage.configure(text=self._message)
                self.btnOK.configure(state="normal")
                return False

        self.lblMessage.configure(text="")
        self.btnOK.configure(state="normal")
        return True

    def __init__(self, top, pZonesIDF, pZonesGUI):
        self._uuid = str(uuid.uuid4())
        ## colours, icons
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#d9d9d9' # X11 color: 'gray85'
        _width = 400
        _height = 300

        self.top = tk.Toplevel(top)
        self.top.transient(top)
        self.top.grab_set()
        uX = (top.winfo_screenwidth() - top.winfo_reqwidth()) / 2
        uY = (top.winfo_screenheight() - top.winfo_reqheight()) / 2
        self.top.geometry("%dx%d+%d+%d" % (_width, _height, uX, uY))

        self.top.title("Zones in the idf file and configuration")

        # no resize window and OnClose event
        # self.top.resizable(False, False)
        self.top.protocol("WM_DELETE_WINDOW", self.OnCancel)

        # variables
        self._confirm = False
        self._error = False
        self._message = ""
        self._zonesIDF = {}
        self._zonesGUI = {}
        for i in pZonesIDF:
            self._zonesIDF[i] = i

        for i in pZonesGUI:
            self._zonesGUI[i] = i
        
        self._zonesIDF = collections.OrderedDict(sorted(self._zonesIDF.items(), key=lambda x: x[1]))
        self._zonesGUI = collections.OrderedDict(sorted(self._zonesGUI.items(), key=lambda x: x[1]))

        # action buttons
        button_width = 76.0
        button_x = ((_width/2.0) - button_width) / 2.0
        self.btnCancel = ttk.Button(self.top, command=self.OnCancel)
        self.btnCancel.place(x=button_x, rely=0.9, height=25, width=button_width)
        self.btnCancel.configure(takefocus="")
        self.btnCancel.configure(text="Cancel")

        self.btnOK = ttk.Button(self.top, command=self.btnOK_OnClick)
        self.btnOK.place(x=(button_x + (_width/2.0)), rely=0.9, height=25, width=button_width)
        self.btnOK.configure(takefocus="")
        self.btnOK.configure(text="OK")

        containerLeft = tk.Frame(self.top)
        self.lblzonesIDF = tk.Label(containerLeft, text="IDF file:") #, relwidth=0.48, anchor="w")
        self.lblzonesIDF.pack()
        self.lstZonesIDF = Utils.UI.Controls.LstBox(containerLeft, sortList=False, list=self._zonesIDF, exportselection=False, height=100)
        self.lstZonesIDF.pack(fill="x", expand=True, side="left")
        containerLeft.place(relx=0.01, rely=0.01, relheight=.8, relwidth=0.48)

        containerRight = tk.Frame(self.top)
        self.lblzonesGUI = tk.Label(containerRight, text="Created by user:")
        self.lblzonesGUI.pack()
        self.lstZonesGUI = Utils.UI.Controls.LstBox(containerRight, sortList=False, list=self._zonesGUI, exportselection=False, height=100)
        self.lstZonesGUI.pack(fill="x", expand=True, side="left")
        containerRight.place(relx=0.51, rely=0.01, relheight=.8, relwidth=0.48)

        containerBtm = tk.Frame(self.top, borderwidth=1, relief="groove", background="#ffffff")
        self.lblMessage = tk.Label(containerBtm, text="ERROR!:", background="#ffffff", foreground="#ff0000")
        self.lblMessage.pack()
        containerBtm.place(relx=0.01, rely=0.82, height=20, relwidth=.98)

        self.compareLists()
        return
# end of FrmListOfZonesVerification