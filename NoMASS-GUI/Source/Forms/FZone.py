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

class FrmZone(object):
    def load(self, id=None, name=None, activities=None, groundFloor=None, windowCount=None, floorArea=None, show=False, enabled=False):
        if id is not None:
            self._id = id

        if name is not None:
            self._name = name
            self.txtname.config(textvariable=self._name, state="disabled")

        if activities is not None:
            self._activities = activities
            self.lstActivities._selectedValues = self._activities
            self.lstActivities.refreshSelection()

        if groundFloor is not None:
            self._groundFloor = groundFloor
            self.chkgroundFloor.config(variable=self._groundFloor, state="normal" if enabled else "disabled")

        if windowCount is not None:
            self._windowCount = windowCount
            self.txtwindowCount.config(textvariable=self._windowCount, state="normal" if enabled else "disabled")

        if floorArea is not None:
            self._floorArea = floorArea
            self.txtfloorArea.config(textvariable=self._floorArea, state="normal" if enabled else "disabled")

        if show:
            self._parentWidget.refreshTabEdit()
            self.show()

    def show(self):
        self._frame.tkraise()

    def __init__(self, master, parent, id=str(uuid.uuid4()), name='', activities='', groundFloor=False, windowCount=0, floorArea=0):
        form_margin_top = 10
        column_width = 25
        padding_outer = 100
        padding_inner = 5
        padding_top = 2
        padding_btm = 2

        self._parentWidget = master

        self._uuid = str(uuid.uuid4())

        self._typeOfClass = tk.IntVar()
        self._id = tk.StringVar()
        self._name = tk.StringVar()
        self._activities = tk.StringVar()
        self._groundFloor = tk.BooleanVar()
        self._windowCount = tk.IntVar()
        self._floorArea = tk.DoubleVar()

        self._typeOfClass = typeOfClass.BUILDING_ZONE
        self._frame = tk.Frame(parent, width=parent.winfo_reqwidth(), height=parent.winfo_reqheight())
        self._frame.grid(row=0, column=0, sticky="nsew")

        containerTemp = tk.Frame(self._frame)
        self.lblname = tk.Label(containerTemp, text="Name:", width=column_width, anchor="w")
        self.lblname.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtname = tk.Entry(containerTemp, justify="right")
        self.txtname.config(textvariable=self._name, state="disabled")
        self.txtname.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblactivities = tk.Label(containerTemp, text="Activities:", width=column_width, anchor="w")
        self.lblactivities.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.lstActivities = Utils.UI.Controls.LstBox(containerTemp, sortList=False, list=Utils.Config.getCatalog("roomActivities"), exportselection=False)
        self.lstActivities.configure(selectmode="extended")
        self.lstActivities.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblgroundFloor = tk.Label(containerTemp, text="Is Ground Floor:", width=column_width, anchor="w")
        self.lblgroundFloor.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.chkgroundFloor = tk.Checkbutton(containerTemp, text="", anchor='w', onvalue=True, offvalue=False, variable=self._groundFloor)
        self.chkgroundFloor.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblwindowCount = tk.Label(containerTemp, text="Window Count:", width=column_width, anchor="w")
        self.lblwindowCount.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtwindowCount = tk.Spinbox(containerTemp, textvariable=self._windowCount, from_=1, to=1000, increment=1, state='readonly', justify='right')
        self.txtwindowCount.pack(fill='x', expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))
        
        containerTemp = tk.Frame(self._frame)
        self.lblfloorArea = tk.Label(containerTemp, text="Floor Area:", width=column_width, anchor="w")
        self.lblfloorArea.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtfloorArea = tk.Entry(containerTemp, textvariable=self._floorArea, justify='right')
        self.txtfloorArea.pack(fill='x', expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        self._id.set(id)
        self._name.set(name)
        self._activities.set(activities)
        self._groundFloor.set(groundFloor)
        self._windowCount.set(windowCount)
        self._floorArea.set(floorArea)

        self._frame.update_idletasks()
        return
# end of FrmZone