import uuid
import os
import sys
if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Utils"))
from CUtils import *

class FrmLog(object):
    @property
    def ID(self):
        return self._uuid

    def write(self, value):
        self.txtLog.insert("end", value + "\n")
        self.txtLog.see("end")

    def __init__(self, parent):
        self._uuid = str(uuid.uuid4())

        self.txtLog = tk.Text(parent, borderwidth=1, relief='groove')
        self.txtLog.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        scrollb = tk.Scrollbar(parent, command=self.txtLog.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txtLog['yscrollcommand'] = scrollb.set
        return
# end of FrmLog
