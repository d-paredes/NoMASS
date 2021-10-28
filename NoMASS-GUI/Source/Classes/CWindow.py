import uuid
import os
import sys
if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Enums"))
from CEnums import *

class CWindow(object):
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
    def aop(self):
        return self._aop.get()
    @aop.setter
    def aop(self, value):
        self._aop.set(value)

    @property
    def bopout(self):
        return self._bopout.get()
    @bopout.setter
    def bopout(self, value):
        self._bopout.set(value)

    @property
    def shapeop(self):
        return self._shapeop.get()
    @shapeop.setter
    def shapeop(self, value):
        self._shapeop.set(value)

    @property
    def a01arr(self):
        return self._a01arr.get()
    @a01arr.setter
    def a01arr(self, value):
        self._a01arr.set(value)

    @property
    def b01inarr(self):
        return self._b01inarr.get()
    @b01inarr.setter
    def b01inarr(self, value):
        self._b01inarr.set(value)

    @property
    def b01outarr(self):
        return self._b01outarr.get()
    @b01outarr.setter
    def b01outarr(self, value):
        self._b01outarr.set(value)

    @property
    def b01absprevarr(self):
        return self._b01absprevarr.get()
    @b01absprevarr.setter
    def b01absprevarr(self, value):
        self._b01absprevarr.set(value)

    @property
    def b01rnarr(self):
        return self._b01rnarr.get()
    @b01rnarr.setter
    def b01rnarr(self, value):
        self._b01rnarr.set(value)

    @property
    def a01int(self):
        return self._a01int.get()
    @a01int.setter
    def a01int(self, value):
        self._a01int.set(value)

    @property
    def b01inint(self):
        return self._b01inint.get()
    @b01inint.setter
    def b01inint(self, value):
        self._b01inint.set(value)

    @property
    def b01outint(self):
        return self._b01outint.get()
    @b01outint.setter
    def b01outint(self, value):
        self._b01outint.set(value)

    @property
    def b01presint(self):
        return self._b01presint.get()
    @b01presint.setter
    def b01presint(self, value):
        self._b01presint.set(value)

    @property
    def b01rnint(self):
        return self._b01rnint.get()
    @b01rnint.setter
    def b01rnint(self, value):
        self._b01rnint.set(value)

    @property
    def a01dep(self):
        return self._a01dep.get()
    @a01dep.setter
    def a01dep(self, value):
        self._a01dep.set(value)

    @property
    def b01outdep(self):
        return self._b01outdep.get()
    @b01outdep.setter
    def b01outdep(self, value):
        self._b01outdep.set(value)

    @property
    def b01absdep(self):
        return self._b01absdep.get()
    @b01absdep.setter
    def b01absdep(self, value):
        self._b01absdep.set(value)

    @property
    def b01gddep(self):
        return self._b01gddep.get()
    @b01gddep.setter
    def b01gddep(self, value):
        self._b01gddep.set(value)

    @property
    def a10dep(self):
        return self._a10dep.get()
    @a10dep.setter
    def a10dep(self, value):
        self._a10dep.set(value)

    @property
    def b10indep(self):
        return self._b10indep.get()
    @b10indep.setter
    def b10indep(self, value):
        self._b10indep.set(value)

    @property
    def b10outdep(self):
        return self._b10outdep.get()
    @b10outdep.setter
    def b10outdep(self, value):
        self._b10outdep.set(value)

    @property
    def b10absdep(self):
        return self._b10absdep.get()
    @b10absdep.setter
    def b10absdep(self, value):
        self._b10absdep.set(value)

    @property
    def b10gddep(self):
        return self._b10gddep.get()
    @b10gddep.setter
    def b10gddep(self, value):
        self._b10gddep.set(value)

    def __init__(self, id=0, name='', aop=0, bopout=0, shapeop=0, a01arr=0, b01inarr=0, b01outarr=0, b01absprevarr=0, b01rnarr=0, a01int=0, b01inint=0, b01outint=0, b01presint=0, b01rnint=0, a01dep=0, b01outdep=0, b01absdep=0, b01gddep=0, a10dep=0, b10indep=0, b10outdep=0, b10absdep=0, b10gddep=0):
        self._uuid = str(uuid.uuid4())
        self._typeOfClass = tk.IntVar()
        self._id = tk.IntVar()
        self._name = tk.StringVar()
        self._aop = tk.DoubleVar()
        self._bopout = tk.DoubleVar()
        self._shapeop = tk.DoubleVar()
        self._a01arr = tk.DoubleVar()
        self._b01inarr = tk.DoubleVar()
        self._b01outarr = tk.DoubleVar()
        self._b01absprevarr = tk.DoubleVar()
        self._b01rnarr = tk.DoubleVar()
        self._a01int = tk.DoubleVar()
        self._b01inint = tk.DoubleVar()
        self._b01outint = tk.DoubleVar()
        self._b01presint = tk.DoubleVar()
        self._b01rnint = tk.DoubleVar()
        self._a01dep = tk.DoubleVar()
        self._b01outdep = tk.DoubleVar()
        self._b01absdep = tk.DoubleVar()
        self._b01gddep = tk.DoubleVar()
        self._a10dep = tk.DoubleVar()
        self._b10indep = tk.DoubleVar()
        self._b10outdep = tk.DoubleVar()
        self._b10absdep = tk.DoubleVar()
        self._b10gddep = tk.DoubleVar()

        self._typeOfClass.set(typeOfClass.MODEL_WINDOW)
        self._id.set(id)
        self._name.set(name)
        self._aop.set(aop)
        self._bopout.set(bopout)
        self._shapeop.set(shapeop)
        self._a01arr.set(a01arr)
        self._b01inarr.set(b01inarr)
        self._b01outarr.set(b01outarr)
        self._b01absprevarr.set(b01absprevarr)
        self._b01rnarr.set(b01rnarr)
        self._a01int.set(a01int)
        self._b01inint.set(b01inint)
        self._b01outint.set(b01outint)
        self._b01presint.set(b01presint)
        self._b01rnint.set(b01rnint)
        self._a01dep.set(a01dep)
        self._b01outdep.set(b01outdep)
        self._b01absdep.set(b01absdep)
        self._b01gddep.set(b01gddep)
        self._a10dep.set(a10dep)
        self._b10indep.set(b10indep)
        self._b10outdep.set(b10outdep)
        self._b10absdep.set(b10absdep)
        self._b10gddep.set(b10gddep)
# end of CWindow
