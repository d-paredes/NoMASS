import uuid
import os
import sys
if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Enums"))
from CEnums import *

class CHeating(object):
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
    def enabled(self):
        return self._enabled.get()
    @enabled.setter
    def enabled(self, value):
        self._enabled.set(value)

    def __init__(self, id=str(uuid.uuid4()), enabled=True):
        self._uuid = id
        self._typeOfClass = tk.IntVar()
        self._id = tk.StringVar()
        self._enabled = tk.BooleanVar()

        self._typeOfClass.set(typeOfClass.MODEL_HEATING)
        self._id.set(id)
        self._enabled.set(enabled)
# end of CHeating

