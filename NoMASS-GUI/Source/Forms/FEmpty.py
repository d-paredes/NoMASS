import uuid
import os
import sys
if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Utils"))
from CUtils import *

class FrmEmpty(object):
    @property
    def ID(self):
        return self._uuid

    @property
    def Frame(self):
        return self._frame

    def load(self, title=None):
        if title is not None:
            self._title.config(text=title)
        self.show()
        return

    def show(self):
        self._frame.tkraise()

    @property
    def title(self):
        return self._title["text"]

    @title.setter
    def title(self, value):
        self._title.config(text=value)

    def __init__(self, parent):
        self._uuid = Utils.Constants.emptyGUID
        self._frame = tk.Frame(parent, width=parent.winfo_reqwidth(), height=parent.winfo_reqheight())
        self._frame.grid(row=0, column=0, sticky="nsew")
        self._title = tk.Label(self._frame, text="")
        self._title.pack(fill='x', expand=True, padx=20, pady=(10,0))
        self._frame.update_idletasks()
        return
# end of FrmEmpty