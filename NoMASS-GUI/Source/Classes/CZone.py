import uuid
import os
import sys
if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Enums"))
from CEnums import *

class CZone(object):
    @property
    def UUID(self):
        return self._uuid

    @property
    def type(self):
        return self._typeOfClass.get()
    @type.setter
    def type(self, value):
        return self._typeOfClass.set(value)

    @property
    def ID(self):
        return self._id.get()
    @ID.setter
    def ID(self, value):
        self._id.set(value)

    @property
    def name(self):
        return self._name.get()
    @name.setter
    def name(self, value):
        self._name.set(value)

    @property
    def activities(self):
        return self._activities.get()
    @activities.setter
    def activities(self, value):
        self._activities.set(value)

    @property
    def groundFloor(self):
        return self._groundFloor.get()
    @groundFloor.setter
    def groundFloor(self, value):
        self._groundFloor.set(value)

    @property
    def windowCount(self):
        return self._windowCount.get()
    @windowCount.setter
    def windowCount(self, value):
        self._windowCount.set(value)

    @property
    def floorArea(self):
        return self._floorArea.get()
    @floorArea.setter
    def floorArea(self, value):
        self._floorArea.set(value)

    def __init__(self, id=str(uuid.uuid4()), name='', activities='', groundFloor=False, windowCount=0, floorArea=0):
        self._uuid = id
        self._typeOfClass = tk.IntVar()
        self._id = tk.StringVar()
        self._name = tk.StringVar()
        self._activities = tk.StringVar()
        self._groundFloor = tk.BooleanVar()
        self._windowCount = tk.IntVar()
        self._floorArea = tk.DoubleVar()

        self._typeOfClass.set(typeOfClass.BUILDING_ZONE)
        self._id.set(id)
        self._name.set(name)
        self._activities.set(activities)
        self._groundFloor.set(groundFloor)
        self._windowCount.set(windowCount)
        self._floorArea.set(floorArea)
# end of CZone
