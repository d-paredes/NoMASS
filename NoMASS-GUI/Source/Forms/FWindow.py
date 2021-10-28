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

class FrmWindow(object):
    def load(self, id=None, name=None, aop=None, bopout=None, shapeop=None, a01arr=None, b01inarr=None, b01outarr=None, b01absprevarr=None, b01rnarr=None, a01int=None, b01inint=None, b01outint=None, b01presint=None, b01rnint=None, a01dep=None, b01outdep=None, b01absdep=None, b01gddep=None, a10dep=None, b10indep=None, b10outdep=None, b10absdep=None, b10gddep=None, show=False):

        if id is not None:
            self._id = id
            self.txtid.config(textvariable=self._id, state="disabled")

        if name is not None:
            self._name = name
            self.txtname.config(textvariable=self._name, state="disabled")

        if aop is not None:
            self._aop = aop
            self.txtaop.config(textvariable=self._aop, state="disabled")

        if bopout is not None:
            self._bopout = bopout
            self.txtbopout.config(textvariable=self._bopout, state="disabled")

        if shapeop is not None:
            self._shapeop = shapeop
            self.txtshapeop.config(textvariable=self._shapeop, state="disabled")

        if a01arr is not None:
            self._a01arr = a01arr
            self.txta01arr.config(textvariable=self._a01arr, state="disabled")

        if b01inarr is not None:
            self._b01inarr = b01inarr
            self.txtb01inarr.config(textvariable=self._b01inarr, state="disabled")

        if b01outarr is not None:
            self._b01outarr = b01outarr
            self.txtb01outarr.config(textvariable=self._b01outarr, state="disabled")

        if b01absprevarr is not None:
            self._b01absprevarr = b01absprevarr
            self.txtb01absprevarr.config(textvariable=self._b01absprevarr, state="disabled")

        if b01rnarr is not None:
            self._b01rnarr = b01rnarr
            self.txtb01rnarr.config(textvariable=self._b01rnarr, state="disabled")

        if a01int is not None:
            self._a01int = a01int
            self.txta01int.config(textvariable=self._a01int, state="disabled")

        if b01inint is not None:
            self._b01inint = b01inint
            self.txtb01inint.config(textvariable=self._b01inint, state="disabled")

        if b01outint is not None:
            self._b01outint = b01outint
            self.txtb01outint.config(textvariable=self._b01outint, state="disabled")

        if b01presint is not None:
            self._b01presint = b01presint
            self.txtb01presint.config(textvariable=self._b01presint, state="disabled")

        if b01rnint is not None:
            self._b01rnint = b01rnint
            self.txtb01rnint.config(textvariable=self._b01rnint, state="disabled")

        if a01dep is not None:
            self._a01dep = a01dep
            self.txta01dep.config(textvariable=self._a01dep, state="disabled")

        if b01outdep is not None:
            self._b01outdep = b01outdep
            self.txtb01outdep.config(textvariable=self._b01outdep, state="disabled")

        if b01absdep is not None:
            self._b01absdep = b01absdep
            self.txtb01absdep.config(textvariable=self._b01absdep, state="disabled")

        if b01gddep is not None:
            self._b01gddep = b01gddep
            self.txtb01gddep.config(textvariable=self._b01gddep, state="disabled")

        if a10dep is not None:
            self._a10dep = a10dep
            self.txta10dep.config(textvariable=self._a10dep, state="disabled")

        if b10indep is not None:
            self._b10indep = b10indep
            self.txtb10indep.config(textvariable=self._b10indep, state="disabled")

        if b10outdep is not None:
            self._b10outdep = b10outdep
            self.txtb10outdep.config(textvariable=self._b10outdep, state="disabled")

        if b10absdep is not None:
            self._b10absdep = b10absdep
            self.txtb10absdep.config(textvariable=self._b10absdep, state="disabled")

        if b10gddep is not None:
            self._b10gddep = b10gddep
            self.txtb10gddep.config(textvariable=self._b10gddep, state="disabled")

        if show:
            self._parentWidget.refreshTabEdit(800)
            self.show()

    def show(self):
        self._frame.tkraise()

    def __init__(self, master, parent, id=0, name='', aop=0, bopout=0, shapeop=0, a01arr=0, b01inarr=0, b01outarr=0, b01absprevarr=0, b01rnarr=0, a01int=0, b01inint=0, b01outint=0, b01presint=0, b01rnint=0, a01dep=0, b01outdep=0, b01absdep=0, b01gddep=0, a10dep=0, b10indep=0, b10outdep=0, b10absdep=0, b10gddep=0):
        form_margin_top = 10
        column_width = 25
        padding_outer = 100
        padding_inner = 5
        padding_top = 2
        padding_btm = 2

        self._parentWidget = master

        self._uuid = str(uuid.uuid4())

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

        self._typeOfClass = typeOfClass.MODEL_WINDOW
        self._frame = tk.Frame(parent, width=parent.winfo_reqwidth(), height=parent.winfo_reqheight())
        self._frame.grid(row=0, column=0, sticky="nsew")

        containerTemp = tk.Frame(self._frame)
        self.lblid = tk.Label(containerTemp, text="id:", width=column_width, anchor="w")
        self.lblid.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtid = tk.Entry(containerTemp, justify="right")
        self.txtid.config(textvariable=self._id, state="disabled")
        self.txtid.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblname = tk.Label(containerTemp, text="name:", width=column_width, anchor="w")
        self.lblname.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtname = tk.Entry(containerTemp, justify="right")
        self.txtname.config(textvariable=self._name, state="disabled")
        self.txtname.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblaop = tk.Label(containerTemp, text="aop:", width=column_width, anchor="w")
        self.lblaop.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtaop = tk.Entry(containerTemp, justify="right")
        self.txtaop.config(textvariable=self._aop, state="disabled")
        self.txtaop.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblbopout = tk.Label(containerTemp, text="bopout:", width=column_width, anchor="w")
        self.lblbopout.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtbopout = tk.Entry(containerTemp, justify="right")
        self.txtbopout.config(textvariable=self._bopout, state="disabled")
        self.txtbopout.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblshapeop = tk.Label(containerTemp, text="shapeop:", width=column_width, anchor="w")
        self.lblshapeop.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtshapeop = tk.Entry(containerTemp, justify="right")
        self.txtshapeop.config(textvariable=self._shapeop, state="disabled")
        self.txtshapeop.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lbla01arr = tk.Label(containerTemp, text="a01arr:", width=column_width, anchor="w")
        self.lbla01arr.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txta01arr = tk.Entry(containerTemp, justify="right")
        self.txta01arr.config(textvariable=self._a01arr, state="disabled")
        self.txta01arr.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblb01inarr = tk.Label(containerTemp, text="b01inarr:", width=column_width, anchor="w")
        self.lblb01inarr.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb01inarr = tk.Entry(containerTemp, justify="right")
        self.txtb01inarr.config(textvariable=self._b01inarr, state="disabled")
        self.txtb01inarr.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblb01outarr = tk.Label(containerTemp, text="b01outarr:", width=column_width, anchor="w")
        self.lblb01outarr.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb01outarr = tk.Entry(containerTemp, justify="right")
        self.txtb01outarr.config(textvariable=self._b01outarr, state="disabled")
        self.txtb01outarr.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblb01absprevarr = tk.Label(containerTemp, text="b01absprevarr:", width=column_width, anchor="w")
        self.lblb01absprevarr.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb01absprevarr = tk.Entry(containerTemp, justify="right")
        self.txtb01absprevarr.config(textvariable=self._b01absprevarr, state="disabled")
        self.txtb01absprevarr.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblb01rnarr = tk.Label(containerTemp, text="b01rnarr:", width=column_width, anchor="w")
        self.lblb01rnarr.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb01rnarr = tk.Entry(containerTemp, justify="right")
        self.txtb01rnarr.config(textvariable=self._b01rnarr, state="disabled")
        self.txtb01rnarr.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lbla01int = tk.Label(containerTemp, text="a01int:", width=column_width, anchor="w")
        self.lbla01int.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txta01int = tk.Entry(containerTemp, justify="right")
        self.txta01int.config(textvariable=self._a01int, state="disabled")
        self.txta01int.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblb01inint = tk.Label(containerTemp, text="b01inint:", width=column_width, anchor="w")
        self.lblb01inint.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb01inint = tk.Entry(containerTemp, justify="right")
        self.txtb01inint.config(textvariable=self._b01inint, state="disabled")
        self.txtb01inint.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblb01outint = tk.Label(containerTemp, text="b01outint:", width=column_width, anchor="w")
        self.lblb01outint.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb01outint = tk.Entry(containerTemp, justify="right")
        self.txtb01outint.config(textvariable=self._b01outint, state="disabled")
        self.txtb01outint.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblb01presint = tk.Label(containerTemp, text="b01presint:", width=column_width, anchor="w")
        self.lblb01presint.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb01presint = tk.Entry(containerTemp, justify="right")
        self.txtb01presint.config(textvariable=self._b01presint, state="disabled")
        self.txtb01presint.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblb01rnint = tk.Label(containerTemp, text="b01rnint:", width=column_width, anchor="w")
        self.lblb01rnint.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb01rnint = tk.Entry(containerTemp, justify="right")
        self.txtb01rnint.config(textvariable=self._b01rnint, state="disabled")
        self.txtb01rnint.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lbla01dep = tk.Label(containerTemp, text="a01dep:", width=column_width, anchor="w")
        self.lbla01dep.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txta01dep = tk.Entry(containerTemp, justify="right")
        self.txta01dep.config(textvariable=self._a01dep, state="disabled")
        self.txta01dep.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblb01outdep = tk.Label(containerTemp, text="b01outdep:", width=column_width, anchor="w")
        self.lblb01outdep.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb01outdep = tk.Entry(containerTemp, justify="right")
        self.txtb01outdep.config(textvariable=self._b01outdep, state="disabled")
        self.txtb01outdep.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblb01absdep = tk.Label(containerTemp, text="b01absdep:", width=column_width, anchor="w")
        self.lblb01absdep.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb01absdep = tk.Entry(containerTemp, justify="right")
        self.txtb01absdep.config(textvariable=self._b01absdep, state="disabled")
        self.txtb01absdep.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblb01gddep = tk.Label(containerTemp, text="b01gddep:", width=column_width, anchor="w")
        self.lblb01gddep.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb01gddep = tk.Entry(containerTemp, justify="right")
        self.txtb01gddep.config(textvariable=self._b01gddep, state="disabled")
        self.txtb01gddep.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lbla10dep = tk.Label(containerTemp, text="a10dep:", width=column_width, anchor="w")
        self.lbla10dep.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txta10dep = tk.Entry(containerTemp, justify="right")
        self.txta10dep.config(textvariable=self._a10dep, state="disabled")
        self.txta10dep.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblb10indep = tk.Label(containerTemp, text="b10indep:", width=column_width, anchor="w")
        self.lblb10indep.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb10indep = tk.Entry(containerTemp, justify="right")
        self.txtb10indep.config(textvariable=self._b10indep, state="disabled")
        self.txtb10indep.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblb10outdep = tk.Label(containerTemp, text="b10outdep:", width=column_width, anchor="w")
        self.lblb10outdep.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb10outdep = tk.Entry(containerTemp, justify="right")
        self.txtb10outdep.config(textvariable=self._b10outdep, state="disabled")
        self.txtb10outdep.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblb10absdep = tk.Label(containerTemp, text="b10absdep:", width=column_width, anchor="w")
        self.lblb10absdep.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb10absdep = tk.Entry(containerTemp, justify="right")
        self.txtb10absdep.config(textvariable=self._b10absdep, state="disabled")
        self.txtb10absdep.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblb10gddep = tk.Label(containerTemp, text="b10gddep:", width=column_width, anchor="w")
        self.lblb10gddep.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb10gddep = tk.Entry(containerTemp, justify="right")
        self.txtb10gddep.config(textvariable=self._b10gddep, state="disabled")
        self.txtb10gddep.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

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

        self._frame.update_idletasks()
        return
# end of FrmWindow