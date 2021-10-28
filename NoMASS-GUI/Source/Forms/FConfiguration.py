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

class FrmConfiguration(object):
    @property
    def ID(self):
        return self._uuid

    @property
    def Frame(self):
        return self._frame

    @property
    def typeOfBuilding(self):
        return self._typeOfBuilding.get()

    @property
    def area(self):
        return self._area.get()

    @property
    def numberOfOccupants(self):
        return self._numberOfOccupants.get()

    @property
    def seed(self):
        return self._seed.get()

    @property
    def timeStepsPerHour(self):
        return self._timeStepsPerHour.get()

    @property
    def beginMonth(self):
        return self._beginMonth.get()

    @property
    def endMonth(self):
        return self._endMonth.get()

    @property
    def beginDay(self):
        return self._beginDay.get()

    @property
    def endDay(self):
        return self._endDay.get()

    @property
    def learn(self):
        return self._learn.get()

    @property
    def save(self):
        return self._save.get()

    @property
    def eplusVersion(self):
        return self._eplusVersion.get()

    @property
    def numberOfReplicates(self):
        return self._numberOfReplicates.get()

    @property
    def numberOfReplicatesRandom(self):
        return self._numberOfReplicatesRandom.get()
    
    def loadObjSimulation(self, objSimulation):
        self._typeOfBuilding.set(objSimulation.typeOfBuilding)
        self._area.set(objSimulation.area)
        self._numberOfOccupants.set(objSimulation.numberOfOccupants)
        self._seed.set(objSimulation.seed)
        self._timeStepsPerHour.set(objSimulation.timeStepsPerHour)
        self._beginMonth.set(objSimulation.beginMonth)
        self._endMonth.set(objSimulation.endMonth)
        self._beginDay.set(objSimulation.beginDay)
        self._endDay.set(objSimulation.endDay)
        self._learn.set(objSimulation.learn)
        self._save.set(objSimulation.save)
        self._eplusVersion.set(objSimulation.eplusVersion)
        self._numberOfReplicates.set(objSimulation.numberOfReplicates)
        self._numberOfReplicatesRandom.set(objSimulation.numberOfReplicatesRandom)        

    def __init__(self, parent, objSimulation):
        form_margin_top = 10
        column_width = 25
        padding_outer = 100
        padding_inner = 5
        padding_top = 2
        padding_btm = 2

        self._uuid = str(uuid.uuid4())
        self._frame = tk.Frame(parent, width=parent.winfo_reqwidth(), height=parent.winfo_reqheight())
        self._frame.pack(fill="both")

        eplusVersions = str(Utils.Config.getValue("Select", "eplusVersion")).split(',')
        typeOfBuilding = str(Utils.Config.getValue("Select", "typeOfBuilding")).split(',')

        self._typeOfBuilding = tk.StringVar()
        self._area = tk.DoubleVar()
        self._numberOfOccupants = tk.IntVar()
        self._seed = tk.DoubleVar()
        self._timeStepsPerHour = tk.IntVar()
        self._beginMonth = tk.IntVar()
        self._endMonth = tk.IntVar()
        self._beginDay = tk.IntVar()
        self._endDay = tk.IntVar()
        self._learn = tk.BooleanVar()
        self._save = tk.BooleanVar()
        self._eplusVersion = tk.StringVar()
        self._numberOfReplicates = tk.IntVar()
        self._numberOfReplicatesRandom = tk.IntVar()

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="Type of Building:", width=column_width, anchor='w')
        lbl.pack(side="left", padx=(padding_outer, padding_inner))
        self.ddlTypeOfBuilding = tk.OptionMenu(containerTemp, self._typeOfBuilding, *typeOfBuilding)
        self.ddlTypeOfBuilding.pack(fill='x', expand=True, side="left", padx=(padding_inner, padding_outer))
        containerTemp.pack(fill='x', pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text=u'Area (m\u00B2):', width=column_width, anchor='w')
        lbl.pack(side="left", padx=(padding_outer, padding_inner))
        self.txtArea = tk.Entry(containerTemp, textvariable=self._area, justify='right')
        self.txtArea.pack(fill='x', expand=True, side="left", padx=(padding_inner, padding_outer))
        containerTemp.pack(fill='x', pady=(padding_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="Number of occupants:", width=column_width, anchor='w')
        lbl.pack(side="left", padx=(padding_outer, padding_inner))
        self.txtNumberOccupants = tk.Spinbox(containerTemp, textvariable=self._numberOfOccupants, from_=1, to=1000, increment=1, state='readonly', justify='right')
        self.txtNumberOccupants.pack(fill='x', expand=True, side="left", padx=(padding_inner, padding_outer))
        containerTemp.pack(fill='x', pady=(padding_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="Seed:", width=column_width, anchor='w')
        lbl.pack(side="left", padx=(padding_outer, padding_inner))
        self.txtSeed = tk.Entry(containerTemp, textvariable=self._seed, justify='right')
        self.txtSeed.pack(fill='x', expand=True, side="left", padx=(padding_inner, padding_outer))
        containerTemp.pack(fill='x', pady=(padding_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="Timesteps per hour:", width=column_width, anchor='w')
        lbl.pack(side="left", padx=(padding_outer, padding_inner))
        self.txtTimeStepsPHour = tk.Spinbox(containerTemp, textvariable=self._timeStepsPerHour, from_=1, to=60, increment=1, state='readonly', justify='right')
        self.txtTimeStepsPHour.pack(fill='x', expand=True, side="left", padx=(padding_inner, padding_outer))
        containerTemp.pack(fill='x', pady=(padding_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="Begin month:", width=column_width, anchor='w')
        lbl.pack(side="left", padx=(padding_outer, padding_inner))
        self.txtBeginMonth = tk.Spinbox(containerTemp, textvariable=self._beginMonth, from_=1, to=12, increment=1, state='readonly', justify='right')
        self.txtBeginMonth.pack(fill='x', expand=True, side="left", padx=(padding_inner, padding_outer))
        containerTemp.pack(fill='x', pady=(padding_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="End month:", width=column_width, anchor='w')
        lbl.pack(side="left", padx=(padding_outer, padding_inner))
        self.txtEndMonth = tk.Spinbox(containerTemp, textvariable=self._endMonth, from_=1, to=12, increment=1, state='readonly', justify='right')
        self.txtEndMonth.pack(fill='x', expand=True, side="left", padx=(padding_inner, padding_outer))
        containerTemp.pack(fill='x', pady=(padding_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="Begin day:", width=column_width, anchor='w')
        lbl.pack(side="left", padx=(padding_outer, padding_inner))
        self.txtBeginDay = tk.Spinbox(containerTemp, textvariable=self._beginDay, from_=1, to=31, increment=1, state='readonly', justify='right')
        self.txtBeginDay.pack(fill='x', expand=True, side="left", padx=(padding_inner, padding_outer))
        containerTemp.pack(fill='x', pady=(padding_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="End day:", width=column_width, anchor='w')
        lbl.pack(side="left", padx=(padding_outer, padding_inner))
        self.txtEndDay = tk.Spinbox(containerTemp, textvariable=self._endDay, from_=1, to=31, increment=1, state='readonly', justify='right')
        self.txtEndDay.pack(fill='x', expand=True, side="left", padx=(padding_inner, padding_outer))
        containerTemp.pack(fill='x', pady=(padding_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="Learn:", width=column_width, anchor='w')
        lbl.pack(side="left", padx=(padding_outer, padding_inner))
        self.chkLearn = tk.Checkbutton(containerTemp, text="", anchor='w', onvalue=True, offvalue=False, variable=self._learn)
        self.chkLearn.pack(fill='x', side="left", padx=(padding_inner, padding_outer))
        containerTemp.pack(fill='x', pady=(padding_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="Save:", width=column_width, anchor='w')
        lbl.pack(side="left", padx=(padding_outer, padding_inner))
        self.chkSave = tk.Checkbutton(containerTemp, text="",  anchor='w', onvalue=True, offvalue=False, variable=self._save)
        self.chkSave.pack(fill='x', side="left", padx=(padding_inner, padding_outer))
        containerTemp.pack(fill='x', pady=(padding_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="EnergyPlus version:", width=column_width, anchor='w')
        lbl.pack(side="left", padx=(padding_outer, padding_inner))
        self.ddlEPlusVersion = tk.OptionMenu(containerTemp, self._eplusVersion, *eplusVersions)
        self.ddlEPlusVersion.pack(fill='x', expand=True, side="left", padx=(padding_inner, padding_outer))
        containerTemp.pack(fill='x', pady=(padding_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="Number of replicates:", width=column_width, anchor='w')
        lbl.pack(side="left", padx=(padding_outer, padding_inner))
        self.txtNumberReplicates = tk.Spinbox(containerTemp, textvariable=self._numberOfReplicates, from_=1, to=1000, increment=1, justify='right', state='disabled')
        self.txtNumberReplicates.pack(fill='x', expand=True, side="left", padx=(padding_inner, padding_outer))
        containerTemp.pack(fill='x', pady=(padding_top, 0))

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="Replicates with random params:", width=column_width, anchor='w')
        lbl.pack(side="left", padx=(padding_outer, padding_inner))
        self.txtNumberReplicatesRandom = tk.Spinbox(containerTemp, textvariable=self._numberOfReplicatesRandom, from_=1, to=1000, increment=1, justify='right')
        self.txtNumberReplicatesRandom.pack(fill='x', expand=True, side="left", padx=(padding_inner, padding_outer))
        containerTemp.pack(fill='x', pady=(padding_top, 0))

        self.loadObjSimulation(objSimulation)
        return
# end of FrmConfiguration