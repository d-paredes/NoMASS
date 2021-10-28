import uuid
import os
import sys
if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Enums"))
from CEnums import *

class CBuilding(object):
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

    def __init__(self, id=0, name=''):
        self._uuid = str(uuid.uuid4())
        self._typeOfClass = tk.IntVar()
        self._id = tk.IntVar()
        self._name = tk.StringVar()

        self._typeOfClass.set(typeOfClass.BUILDING)
        self._id.set(id)
        self._name.set(name)
# end of CBuilding
