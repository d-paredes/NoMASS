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

class FrmHeating(object):
    def load(self, varEnabled, show=False):
        self._enabled = varEnabled
        self.chkEnabled.config(variable=self._enabled)

        if show:
            self._parentWidget.refreshTabEdit()
            self.show()

    def show(self):
        self._frame.tkraise()

    def __init__(self, master, parent, enabled=False):
        form_margin_top = 10
        column_width = 25
        padding_outer = 100
        padding_inner = 5
        padding_top = 2
        padding_btm = 2

        self._parentWidget = master

        self._enabled = tk.BooleanVar()

        self._uuid = str(uuid.uuid4())
        self._typeOfClass = typeOfClass.MODEL_HEATING
        self._frame = tk.Frame(parent, width=parent.winfo_reqwidth(), height=parent.winfo_reqheight())
        self._frame.grid(row=0, column=0, sticky="nsew")

        containerTemp = tk.Frame(self._frame)
        lbl = tk.Label(containerTemp, text="Enabled:", width=column_width, anchor='w')
        lbl.pack(side="left", padx=(2*padding_inner, padding_inner))
        self.chkEnabled = tk.Checkbutton(containerTemp, text="", anchor='w', onvalue=True, offvalue=False, variable=self._enabled)
        self.chkEnabled.pack(side="left", expand=tk.TRUE)
        containerTemp.pack(fill='x', padx=padding_outer, pady=(form_margin_top, 0))

        self._enabled.set(enabled)

        self._frame.update_idletasks()
        return
# end of FrmHeating