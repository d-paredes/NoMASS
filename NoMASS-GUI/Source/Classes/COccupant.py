import uuid
import os
import sys
if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Enums"))
from CEnums import *

class COccupant(object):
    def UUID(self):
    	return self.uuid

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
    def zoneId(self):
    	return self._zoneId.get()
    @zoneId.setter
    def zoneId(self, value):
    	self._zoneId.set(value)

    @property
    def zone(self):
    	return self._zone.get()
    @zone.setter
    def zone(self, value):
    	self._zone.set(value)

    @property
    def power(self):
    	return self._power.get()
    @power.setter
    def power(self, value):
    	self._power.set(value)

    @property
    def windowId(self):
    	return self._windowId.get()
    @windowId.setter
    def windowId(self, value):
    	self._windowId.set(value)

    @property
    def window(self):
    	return self._window.get()
    @window.setter
    def window(self, value):
    	self._window.set(value)

    @property
    def shadeId(self):
    	return self._shadeId.get()
    @shadeId.setter
    def shadeId(self, value):
    	self._shadeId.set(value)

    @property
    def shade(self):
    	return self._shade.get()
    @shade.setter
    def shade(self, value):
    	self._shade.set(value)

    @property
    def activityId(self):
    	return self._activityId.get()
    @activityId.setter
    def activityId(self, value):
    	self._activityId.set(value)

    # @property
    # def activityName(self):
    #     return self._activityName.get()
    # @activityName.setter
    # def activityName(self, value):
    #     self._activityName.set(value)

    @property
    def sex(self):
    	return self._sex.get()
    @sex.setter
    def sex(self, value):
    	self._sex.set(value)

    @property
    def familyID(self):
    	return self._familyID.get()
    @familyID.setter
    def familyID(self, value):
    	self._familyID.set(value)

    @property
    def educationID(self):
    	return self._educationID.get()
    @educationID.setter
    def educationID(self, value):
    	self._educationID.set(value)

    @property
    def ageGroup(self):
    	return self._ageID.get()
    @ageGroup.setter
    def ageGroup(self, value):
    	self._ageID.set(value)

    @property
    def ownComputer(self):
    	return self._ownComputer.get()
    @ownComputer.setter
    def ownComputer(self, value):
    	self._ownComputer.set(value)

    @property
    def isRetired(self):
    	return self._isRetired.get()
    @isRetired.setter
    def isRetired(self, value):
    	self._isRetired.set(value)

    @property
    def isMarried(self):
    	return self._isMarried.get()
    @isMarried.setter
    def isMarried(self, value):
    	self._isMarried.set(value)

    @property
    def isUnEmployed(self):
    	return self._isUnEmployed.get()
    @isUnEmployed.setter
    def isUnEmployed(self, value):
    	self._isUnEmployed.set(value)


    def __init__(self, id=0, name='', zoneId='', zone='', power=0, windowId='', window='', shadeId='', shade='', activityId='', sex='', familyID='', educationID='', ageGroup='', ownComputer=False, isRetired=False, isMarried=False, isUnEmployed=False):
        self._uuid = str(uuid.uuid4())
        self._typeOfClass = tk.IntVar()
        self._id = tk.IntVar()
        self._name = tk.StringVar()
        self._zoneId = tk.StringVar()
        self._zone = tk.StringVar()
        self._power = tk.DoubleVar()
        self._windowId = tk.StringVar()
        self._window = tk.StringVar()
        self._shadeId = tk.StringVar()
        self._shade = tk.StringVar()
        self._activityId = tk.StringVar()
        self._sex = tk.StringVar()
        self._familyID = tk.StringVar()
        self._educationID = tk.StringVar()
        self._ageID = tk.StringVar()
        self._ownComputer = tk.BooleanVar()
        self._isRetired = tk.BooleanVar()
        self._isMarried = tk.BooleanVar()
        self._isUnEmployed = tk.BooleanVar()

        self._typeOfClass.set(typeOfClass.BUILDING_OCCUPANT)
        self._id.set(id)
        self._name.set(name)
        self._zoneId.set(zoneId)
        self._zone.set(zone)
        self._power.set(power)
        self._windowId.set(windowId)
        self._window.set(window)
        self._shadeId.set(shadeId)
        self._shade.set(shade)
        self._activityId.set(activityId)
        self._sex.set(sex)
        self._familyID.set(familyID)
        self._educationID.set(educationID)
        self._ageID.set(ageGroup)
        self._ownComputer.set(ownComputer)
        self._isRetired.set(isRetired)
        self._isMarried.set(isMarried)
        self._isUnEmployed.set(isUnEmployed)
# end of COccupant
