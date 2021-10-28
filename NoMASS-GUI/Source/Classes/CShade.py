import uuid
import os
import sys
if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Enums"))
from CEnums import *

class CShade(object):
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
    def b01sarr(self):
    	return self._b01sarr.get()
    @b01sarr.setter
    def b01sarr(self, value):
    	self._b01sarr.set(value)

    @property
    def a10arr(self):
    	return self._a10arr.get()
    @a10arr.setter
    def a10arr(self, value):
    	self._a10arr.set(value)

    @property
    def b10inarr(self):
    	return self._b10inarr.get()
    @b10inarr.setter
    def b10inarr(self, value):
    	self._b10inarr.set(value)

    @property
    def b10sarr(self):
    	return self._b10sarr.get()
    @b10sarr.setter
    def b10sarr(self, value):
    	self._b10sarr.set(value)

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
    def b01sint(self):
    	return self._b01sint.get()
    @b01sint.setter
    def b01sint(self, value):
    	self._b01sint.set(value)

    @property
    def a10int(self):
    	return self._a10int.get()
    @a10int.setter
    def a10int(self, value):
    	self._a10int.set(value)

    @property
    def b10inint(self):
    	return self._b10inint.get()
    @b10inint.setter
    def b10inint(self, value):
    	self._b10inint.set(value)

    @property
    def b10sint(self):
    	return self._b10sint.get()
    @b10sint.setter
    def b10sint(self, value):
    	self._b10sint.set(value)

    @property
    def afullraise(self):
    	return self._afullraise.get()
    @afullraise.setter
    def afullraise(self, value):
    	self._afullraise.set(value)

    @property
    def boutfullraise(self):
    	return self._boutfullraise.get()
    @boutfullraise.setter
    def boutfullraise(self, value):
    	self._boutfullraise.set(value)

    @property
    def bsfullraise(self):
    	return self._bsfullraise.get()
    @bsfullraise.setter
    def bsfullraise(self, value):
    	self._bsfullraise.set(value)

    @property
    def bsfulllower(self):
    	return self._bsfulllower.get()
    @bsfulllower.setter
    def bsfulllower(self, value):
    	self._bsfulllower.set(value)

    @property
    def boutfulllower(self):
    	return self._boutfulllower.get()
    @boutfulllower.setter
    def boutfulllower(self, value):
    	self._boutfulllower.set(value)

    @property
    def afulllower(self):
    	return self._afulllower.get()
    @afulllower.setter
    def afulllower(self, value):
    	self._afulllower.set(value)

    @property
    def aSFlower(self):
    	return self._aSFlower.get()
    @aSFlower.setter
    def aSFlower(self, value):
    	self._aSFlower.set(value)

    @property
    def bSFlower(self):
    	return self._bSFlower.get()
    @bSFlower.setter
    def bSFlower(self, value):
    	self._bSFlower.set(value)

    @property
    def shapelower(self):
    	return self._shapelower.get()
    @shapelower.setter
    def shapelower(self, value):
    	self._shapelower.set(value)


    def __init__(self, id=0, name='', a01arr=0, b01inarr=0, b01sarr=0, a10arr=0, b10inarr=0, b10sarr=0, a01int=0, b01inint=0, b01sint=0, a10int=0, b10inint=0, b10sint=0, afullraise=0, boutfullraise=0, bsfullraise=0, bsfulllower=0, boutfulllower=0, afulllower=0, aSFlower=0, bSFlower=0, shapelower=0):
        self._uuid = str(uuid.uuid4())
        self._typeOfClass = tk.IntVar()
        self._id = tk.IntVar()
        self._name = tk.StringVar()
        self._a01arr = tk.DoubleVar()
        self._b01inarr = tk.DoubleVar()
        self._b01sarr = tk.DoubleVar()
        self._a10arr = tk.DoubleVar()
        self._b10inarr = tk.DoubleVar()
        self._b10sarr = tk.DoubleVar()
        self._a01int = tk.DoubleVar()
        self._b01inint = tk.DoubleVar()
        self._b01sint = tk.DoubleVar()
        self._a10int = tk.DoubleVar()
        self._b10inint = tk.DoubleVar()
        self._b10sint = tk.DoubleVar()
        self._afullraise = tk.DoubleVar()
        self._boutfullraise = tk.DoubleVar()
        self._bsfullraise = tk.DoubleVar()
        self._bsfulllower = tk.DoubleVar()
        self._boutfulllower = tk.DoubleVar()
        self._afulllower = tk.DoubleVar()
        self._aSFlower = tk.DoubleVar()
        self._bSFlower = tk.DoubleVar()
        self._shapelower = tk.DoubleVar()

        self._typeOfClass.set(typeOfClass.MODEL_SHADE)
        self._id.set(id)
        self._name.set(name)
        self._a01arr.set(a01arr)
        self._b01inarr.set(b01inarr)
        self._b01sarr.set(b01sarr)
        self._a10arr.set(a10arr)
        self._b10inarr.set(b10inarr)
        self._b10sarr.set(b10sarr)
        self._a01int.set(a01int)
        self._b01inint.set(b01inint)
        self._b01sint.set(b01sint)
        self._a10int.set(a10int)
        self._b10inint.set(b10inint)
        self._b10sint.set(b10sint)
        self._afullraise.set(afullraise)
        self._boutfullraise.set(boutfullraise)
        self._bsfullraise.set(bsfullraise)
        self._bsfulllower.set(bsfulllower)
        self._boutfulllower.set(boutfulllower)
        self._afulllower.set(afulllower)
        self._aSFlower.set(aSFlower)
        self._bSFlower.set(bSFlower)
        self._shapelower.set(shapelower)
# end of CShade