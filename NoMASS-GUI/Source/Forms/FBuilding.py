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

class FrmBuilding(object):
    def load(self, id=None, name=None, show=False):
        if id is not None:
            self._id = id

        if name is not None:
            self._name = name
            self.txtname.config(textvariable=self._name, state="disabled")

        if show:
            self._parentWidget.refreshTabEdit()
            self.show()

    def show(self):
        self._frame.tkraise()

    def __init__(self, master, parent, id=0, name='', ):
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

        self._typeOfClass = typeOfClass.BUILDING
        self._frame = tk.Frame(parent, width=parent.winfo_reqwidth(), height=parent.winfo_reqheight())
        self._frame.grid(row=0, column=0, sticky="nsew")

        containerTemp = tk.Frame(self._frame)
        self.lblname = tk.Label(containerTemp, text="Name:", width=column_width, anchor="w")
        self.lblname.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.txtname = tk.Entry(containerTemp, justify="right")
        self.txtname.config(textvariable=self._name, state="disabled")
        self.txtname.pack(fill="x", expand=True, side="left")
        containerTemp.pack(fill="x", padx=padding_outer, pady=(form_margin_top, 0))

        self._id.set(id)
        self._name.set(name)

        self._frame.update_idletasks()
        return
# end of FrmBuilding
