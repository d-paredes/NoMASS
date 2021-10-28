import uuid
import os
import sys
if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Enums"))
from CEnums import *

class COccupantTemplate(object):
    @property
    def UUID(self):
    	return self._uuid
    @UUID.setter
    def UUID(self, value):
        self._uuid = value

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
    def description(self):
    	return self._description.get()
    @description.setter
    def description(self, value):
    	self._description.set(value)

    @property
    def categoryID(self):
    	return self._categoryID.get()
    @categoryID.setter
    def categoryID(self, value):
    	self._categoryID.set(value)

    @property
    def category(self):
    	return self._category.get()
    @category.setter
    def category(self, value):
    	self._category.set(value)

    @property
    def regionID(self):
    	return self._regionID.get()
    @regionID.setter
    def regionID(self, value):
    	self._regionID.set(value)

    @property
    def region(self):
    	return self._region.get()
    @region.setter
    def region(self, value):
    	self._region.set(value)

    @property
    def sectorID(self):
    	return self._sectorID.get()
    @sectorID.setter
    def sectorID(self, value):
    	self._sectorID.set(value)

    @property
    def sector(self):
    	return self._sector.get()
    @sector.setter
    def sector(self, value):
    	self._sector.set(value)

    @property
    def occupants(self):
    	return self._occupants
    @occupants.setter
    def occupants(self, array):
    	self._occupants = array


    def __init__(self, id=0, name='', description='', categoryID='', category='', regionID='', region='', sectorID='', sector='', occupants=None): # power=0, zoneId='',
        self._uuid = str(uuid.uuid4())
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

        self._occupants = []
        if occupants is not None:
            self._occupants = occupants

        self._typeOfClass.set(typeOfClass.BUILDING_OCCUPANTTEMPLATE)
        self._id.set(id)
        self._name.set(name)
        self._description.set(description)
        self._categoryID.set(categoryID)
        self._category.set(category)
        self._regionID.set(regionID)
        self._region.set(region)
        self._sectorID.set(sectorID)
        self._sector.set(sector)
# end of COccupantTemplate
