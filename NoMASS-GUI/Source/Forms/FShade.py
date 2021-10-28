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

class FrmShade(object):
    def load(self, id=0, name='', a01arr=0, b01inarr=0, b01sarr=0, a10arr=0, b10inarr=0, b10sarr=0, a01int=0, b01inint=0, b01sint=0, a10int=0, b10inint=0, b10sint=0, afullraise=0, boutfullraise=0, bsfullraise=0, bsfulllower=0, boutfulllower=0, afulllower=0, aSFlower=0, bSFlower=0, shapelower=0, show=False):
        if id is not None:
            self._id = id
            self.txtid.config(textvariable=self._id, state="disabled")

        if name is not None:
            self._name = name
            self.txtname.config(textvariable=self._name, state="disabled")

        if a01arr is not None:
            self._a01arr = a01arr
            self.txta01arr.config(textvariable=self._a01arr, state="disabled")

        if b01inarr is not None:
            self._b01inarr = b01inarr
            self.txtb01inarr.config(textvariable=self._b01inarr, state="disabled")

        if b01sarr is not None:
            self._b01sarr = b01sarr
            self.txtb01sarr.config(textvariable=self._b01sarr, state="disabled")

        if a10arr is not None:
            self._a10arr = a10arr
            self.txta10arr.config(textvariable=self._a10arr, state="disabled")

        if b10inarr is not None:
            self._b10inarr = b10inarr
            self.txtb10inarr.config(textvariable=self._b10inarr, state="disabled")

        if b10sarr is not None:
            self._b10sarr = b10sarr
            self.txtb10sarr.config(textvariable=self._b10sarr, state="disabled")

        if a01int is not None:
            self._a01int = a01int
            self.txta01int.config(textvariable=self._a01int, state="disabled")

        if b01inint is not None:
            self._b01inint = b01inint
            self.txtb01inint.config(textvariable=self._b01inint, state="disabled")

        if b01sint is not None:
            self._b01sint = b01sint
            self.txtb01sint.config(textvariable=self._b01sint, state="disabled")

        if a10int is not None:
            self._a10int = a10int
            self.txta10int.config(textvariable=self._a10int, state="disabled")

        if b10inint is not None:
            self._b10inint = b10inint
            self.txtb10inint.config(textvariable=self._b10inint, state="disabled")

        if b10sint is not None:
            self._b10sint = b10sint
            self.txtb10sint.config(textvariable=self._b10sint, state="disabled")

        if afullraise is not None:
            self._afullraise = afullraise
            self.txtafullraise.config(textvariable=self._afullraise, state="disabled")

        if boutfullraise is not None:
            self._boutfullraise = boutfullraise
            self.txtboutfullraise.config(textvariable=self._boutfullraise, state="disabled")

        if bsfullraise is not None:
            self._bsfullraise = bsfullraise
            self.txtbsfullraise.config(textvariable=self._bsfullraise, state="disabled")

        if bsfulllower is not None:
            self._bsfulllower = bsfulllower
            self.txtbsfulllower.config(textvariable=self._bsfulllower, state="disabled")

        if boutfulllower is not None:
            self._boutfulllower = boutfulllower
            self.txtboutfulllower.config(textvariable=self._boutfulllower, state="disabled")

        if afulllower is not None:
            self._afulllower = afulllower
            self.txtafulllower.config(textvariable=self._afulllower, state="disabled")

        if aSFlower is not None:
            self._aSFlower = aSFlower
            self.txtaSFlower.config(textvariable=self._aSFlower, state="disabled")

        if bSFlower is not None:
            self._bSFlower = bSFlower
            self.txtbSFlower.config(textvariable=self._bSFlower, state="disabled")

        if shapelower is not None:
            self._shapelower = shapelower
            self.txtshapelower.config(textvariable=self._shapelower, state="disabled")

        if show:
            self._parentWidget.refreshTabEdit(800)
            self.show()

    def show(self):
        self._frame.tkraise()

    def __init__(self, master, parent, id=0, name='', a01arr=0, b01inarr=0, b01sarr=0, a10arr=0, b10inarr=0, b10sarr=0, a01int=0, b01inint=0, b01sint=0, a10int=0, b10inint=0, b10sint=0, afullraise=0, boutfullraise=0, bsfullraise=0, bsfulllower=0, boutfulllower=0, afulllower=0, aSFlower=0, bSFlower=0, shapelower=0):
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

        self._uuid = str(uuid.uuid4())
        self._typeOfClass = typeOfClass.MODEL_SHADE
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
        self.lblb01sarr = tk.Label(containerTemp, text="b01sarr:", width=column_width, anchor="w")
        self.lblb01sarr.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb01sarr = tk.Entry(containerTemp, justify="right")
        self.txtb01sarr.config(textvariable=self._b01sarr, state="disabled")
        self.txtb01sarr.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lbla10arr = tk.Label(containerTemp, text="a10arr:", width=column_width, anchor="w")
        self.lbla10arr.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txta10arr = tk.Entry(containerTemp, justify="right")
        self.txta10arr.config(textvariable=self._a10arr, state="disabled")
        self.txta10arr.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblb10inarr = tk.Label(containerTemp, text="b10inarr:", width=column_width, anchor="w")
        self.lblb10inarr.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb10inarr = tk.Entry(containerTemp, justify="right")
        self.txtb10inarr.config(textvariable=self._b10inarr, state="disabled")
        self.txtb10inarr.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblb10sarr = tk.Label(containerTemp, text="b10sarr:", width=column_width, anchor="w")
        self.lblb10sarr.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb10sarr = tk.Entry(containerTemp, justify="right")
        self.txtb10sarr.config(textvariable=self._b10sarr, state="disabled")
        self.txtb10sarr.pack(fill="x", expand=True, side="left")
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
        self.lblb01sint = tk.Label(containerTemp, text="b01sint:", width=column_width, anchor="w")
        self.lblb01sint.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb01sint = tk.Entry(containerTemp, justify="right")
        self.txtb01sint.config(textvariable=self._b01sint, state="disabled")
        self.txtb01sint.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lbla10int = tk.Label(containerTemp, text="a10int:", width=column_width, anchor="w")
        self.lbla10int.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txta10int = tk.Entry(containerTemp, justify="right")
        self.txta10int.config(textvariable=self._a10int, state="disabled")
        self.txta10int.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblb10inint = tk.Label(containerTemp, text="b10inint:", width=column_width, anchor="w")
        self.lblb10inint.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb10inint = tk.Entry(containerTemp, justify="right")
        self.txtb10inint.config(textvariable=self._b10inint, state="disabled")
        self.txtb10inint.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblb10sint = tk.Label(containerTemp, text="b10sint:", width=column_width, anchor="w")
        self.lblb10sint.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtb10sint = tk.Entry(containerTemp, justify="right")
        self.txtb10sint.config(textvariable=self._b10sint, state="disabled")
        self.txtb10sint.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblafullraise = tk.Label(containerTemp, text="afullraise:", width=column_width, anchor="w")
        self.lblafullraise.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtafullraise = tk.Entry(containerTemp, justify="right")
        self.txtafullraise.config(textvariable=self._afullraise, state="disabled")
        self.txtafullraise.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblboutfullraise = tk.Label(containerTemp, text="boutfullraise:", width=column_width, anchor="w")
        self.lblboutfullraise.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtboutfullraise = tk.Entry(containerTemp, justify="right")
        self.txtboutfullraise.config(textvariable=self._boutfullraise, state="disabled")
        self.txtboutfullraise.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblbsfullraise = tk.Label(containerTemp, text="bsfullraise:", width=column_width, anchor="w")
        self.lblbsfullraise.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtbsfullraise = tk.Entry(containerTemp, justify="right")
        self.txtbsfullraise.config(textvariable=self._bsfullraise, state="disabled")
        self.txtbsfullraise.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblbsfulllower = tk.Label(containerTemp, text="bsfulllower:", width=column_width, anchor="w")
        self.lblbsfulllower.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtbsfulllower = tk.Entry(containerTemp, justify="right")
        self.txtbsfulllower.config(textvariable=self._bsfulllower, state="disabled")
        self.txtbsfulllower.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblboutfulllower = tk.Label(containerTemp, text="boutfulllower:", width=column_width, anchor="w")
        self.lblboutfulllower.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtboutfulllower = tk.Entry(containerTemp, justify="right")
        self.txtboutfulllower.config(textvariable=self._boutfulllower, state="disabled")
        self.txtboutfulllower.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblafulllower = tk.Label(containerTemp, text="afulllower:", width=column_width, anchor="w")
        self.lblafulllower.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtafulllower = tk.Entry(containerTemp, justify="right")
        self.txtafulllower.config(textvariable=self._afulllower, state="disabled")
        self.txtafulllower.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblaSFlower = tk.Label(containerTemp, text="aSFlower:", width=column_width, anchor="w")
        self.lblaSFlower.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtaSFlower = tk.Entry(containerTemp, justify="right")
        self.txtaSFlower.config(textvariable=self._aSFlower, state="disabled")
        self.txtaSFlower.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblbSFlower = tk.Label(containerTemp, text="bSFlower:", width=column_width, anchor="w")
        self.lblbSFlower.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtbSFlower = tk.Entry(containerTemp, justify="right")
        self.txtbSFlower.config(textvariable=self._bSFlower, state="disabled")
        self.txtbSFlower.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        containerTemp = tk.Frame(self._frame)
        self.lblshapelower = tk.Label(containerTemp, text="shapelower:", width=column_width, anchor="w")
        self.lblshapelower.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtshapelower = tk.Entry(containerTemp, justify="right")
        self.txtshapelower.config(textvariable=self._shapelower, state="disabled")
        self.txtshapelower.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

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

        self._frame.update_idletasks()
        return
# end of FrmShade