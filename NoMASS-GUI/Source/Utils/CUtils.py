import sys
# import ConfigParser updated on 18.10.2021 daps
import os
import platform
import collections

if sys.version_info[0] == 3:
    import tkinter as tk
    from tkinter import messagebox
    from tkinter import filedialog
    from xml.etree import ElementTree
    from tkinter import ttk
    from tkinter import StringVar, DoubleVar, IntVar, BooleanVar
    import configparser as ConfigParser  # updated on 18.10.2021 daps
else:
    import Tkinter as tk
    import tkMessageBox as messagebox
    import tkFileDialog as filedialog
    from xml.etree import cElementTree as ElementTree
    import ttk as ttk
    from Tkinter import StringVar, DoubleVar, IntVar, BooleanVar
    import ConfigParser  # updated on 18.10.2021 daps

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Tooltip"))
from CToolTip import *


class Utils:
    class Constants:
        emptyGUID = "00000000-0000-0000-0000-000000000000"

        @staticmethod
        def transparentColour():
            if str(platform.system().lower()).startswith('linux'):
                return "#0f0"

            if str(platform.system().lower()).startswith('windows'):
                return "#fff"
            else:
                return "systemTransparent"

    class Functions:
        @staticmethod
        def concatenateDict(dictA, dictB):
            output = dictA.copy()
            output.update(dictB.copy())
            return output

        @staticmethod
        def subtractDict(dictA, dictB):
            output = {}
            for _key, _value in dictA.copy().items():
                if _key in dictB:
                    output[_key] = _value
            return output

    class IO:
        @staticmethod
        def isLinux():
            return str(platform.system().lower()).startswith('linux')

        @staticmethod
        def isWindows():
            return str(platform.system().lower()).startswith('windows')

        @staticmethod
        def isMacOS():
            return str(platform.system().lower()).startswith('darwin')

        @staticmethod
        def baseFilename(path):
            return os.path.basename(path)

        @staticmethod
        def folderPath(path):
            # return os.path.abspath(path)
            return os.path.dirname(path)

        @staticmethod
        def filename(path):
            base = Utils.IO.baseFilename(path)
            return os.path.splitext(base)[0]

        @staticmethod
        def fileExtension(path):
            base = Utils.IO.baseFilename(path)
            return os.path.splitext(base)[1]

    class Config:

        @staticmethod
        def getDefaultWindowSize():
            return Utils.Config.getValue('Application', 'windowSize')

        @staticmethod
        def getWindowTitle():
            szTitle = str(Utils.Config.getValue('Application', 'windowTitle')) + ' -- ' + str(
                Utils.Config.getValue('Application', 'year'))
            return szTitle

        @staticmethod
        def getAppLocation():
            parentDirectory = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
            return parentDirectory

        @staticmethod
        def getDefaultWeatherFile():
            return str(Utils.Config.getValue("Default", "weatherFilename"))

        @staticmethod
        def getDefaultIDF():
            return str(Utils.Config.getValue("Default", "idfFilename"))

        @staticmethod
        def getDefaultOutputDirectory():
            parentDirectory = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
            return os.path.join(parentDirectory, "output")

        @staticmethod
        def getEPlusLocation():
            return str(Utils.Config.getValue('Default', 'eplusLocation'))

        @staticmethod
        def getDefaultOccupantDensity():
            return float(Utils.Config.getValue("Default", "occupantDensity"))

        @staticmethod
        def getValue(section, variable):
            config = ConfigParser.RawConfigParser()
            config.read(os.path.join(Utils.Config.getAppLocation(), "settings.cfg"))
            return config.get(section, variable)

        @staticmethod
        def readConfigFile(filename):
            config = ConfigParser.RawConfigParser()
            config.read(filename)
            return config

        @staticmethod
        def getTooltip(variable):
            config = ConfigParser.RawConfigParser()
            config.read('settings.cfg')
            try:
                return config.get("Tooltips", variable)
            except:
                return ""

        @staticmethod
        def getConfigurationFile(fileName, item=None):
            parentDirectory = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
            xmlFile = os.path.join(parentDirectory, os.path.join("data", os.path.join("Config", fileName)))
            if not os.path.exists(xmlFile):
                raise Exception(xmlFile + " doesn\'t exists!")
                return

            tree = ElementTree.parse(xmlFile)
            root = tree.getroot()

            if item is not None:
                root = root.find(item)
                if root is None:
                    raise Exception(item + " not found!")
                    return
            return root

        @staticmethod
        def getConfigurationXMLFile(item=None):
            return Utils.Config.getXMLFile("data.xml", item)

        @staticmethod
        def getAgentTemplatesXMLFile(item=None):
            return Utils.Config.getXMLFile("profiles.xml", item)

        ## \brief Return list from the configuration file
        # Return a list of options from the configuration file used in DropDownList controls
        # \param self
        # \param szCatalog Name of the list
        # \param parentID parentID to filter the list chosen
        @staticmethod
        def getCatalog(szName, parentID=None):
            try:
                XMLtree
            except NameError:
                XMLtree = None

            if XMLtree == None:
                parentDirectory = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
                # print("---->",os.path.dirname(os.path.realpath(__file__)), os.path.split(os.path.dirname(os.path.realpath(__file__)))[0])
                xmlFile = os.path.join(parentDirectory, os.path.join("data", os.path.join("Config", "data.xml")))
                if not os.path.exists(xmlFile):
                    raise Exception(parentDirectory + '/data/Config/' + 'data.xml doesn\'t exists!')
                    return

                XMLtree = ElementTree.parse(xmlFile)
                XMLroot = XMLtree.getroot()

            XMLcatalog = XMLroot.find(szName)
            if XMLcatalog is None:
                raise Exception(szName + ' not found!')
                return

            pDict = {}
            for _element in XMLcatalog:
                if (parentID is None) or \
                        (parentID is not None and _element.find('parentID').text == parentID):
                    pDict[_element.find('id').text] = _element.find('name').text

            # sort dictionary by value, not key
            return collections.OrderedDict(sorted(pDict.items(), key=lambda x: x[1]))  # , reverse=True))

        @staticmethod
        def getCollection(szName):
            try:
                XMLtree
            except NameError:
                XMLtree = None

            if XMLtree == None:
                parentDirectory = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
                xmlFile = os.path.join(parentDirectory, os.path.join("data", os.path.join("Config", "data.xml")))
                if not os.path.exists(xmlFile):
                    raise Exception(parentDirectory + '/data/Config/' + 'data.xml doesn\'t exists!')
                    return

                XMLtree = ElementTree.parse(xmlFile)
                XMLroot = XMLtree.getroot()

            XMLcatalog = XMLroot.find(szName)
            if XMLcatalog is None:
                raise Exception(szName + ' not found!')
                return

            pCollection = []
            pFields = []
            for child in XMLcatalog:
                pDict = {}
                for data in child:
                    pDict[data.tag] = data.text
                    if len(pCollection) == 0:
                        pFields.append(data.tag)
                pCollection.append(pDict)

            # sort dictionary by value, not key
            # return collections.OrderedDict(sorted(pDict.items(), key=lambda x: x[1])) #, reverse=True))
            return pCollection, pFields

    class XML:
        @staticmethod
        def setIndentation(element, level=0):
            i = "\n" + level * "  "
            if len(element):
                if not element.text or not element.text.strip():
                    element.text = i + "  "
                if not element.tail or not element.tail.strip():
                    element.tail = i
                for element in element:
                    Utils.XML.setIndentation(element, level + 1)
                if not element.tail or not element.tail.strip():
                    element.tail = i
            else:
                if level and (not element.tail or not element.tail.strip()):
                    element.tail = i

    class UI:
        @staticmethod
        def createMainMenuBar(parent, commandNew, commandOpen, commandSave, commandExit):
            menubar = tk.Menu(parent)
            filemenu = tk.Menu(menubar, tearoff=0)
            filemenu.add_command(label="New", command=commandNew)
            filemenu.add_command(label="Open", command=commandOpen)
            filemenu.add_command(label="Save", command=commandSave)
            filemenu.add_separator()
            filemenu.add_command(label="Exit", command=commandExit)
            menubar.add_cascade(label="File", menu=filemenu)
            return menubar

        class Controls:
            @staticmethod
            def ImageButton(parent, imageData, command, toolTip=None):
                photo = tk.PhotoImage(data=imageData)
                newButton = tk.Button(parent, relief='flat', image=photo, command=command)  # 918
                newButton.image = photo
                if toolTip is not None:
                    createToolTip(newButton, toolTip)
                return newButton

            # end of ImageButton

            class DropDownList(ttk.Combobox, object):
                def OnSelectedIndexChanged(self, event=None):
                    _text = self.get()
                    _value = list(self._kvData.keys())[list(self._kvData.values()).index(_text)]#updated 18.10.2021 daps list

                    exists = self.getElementByText(self._textVariable.get())

                    if exists is not None:
                        self._value.set(exists[0])
                        self._text.set(exists[1])

                        self._keyVariable.set(self._value.get())

                    if self._nestedControlID is not None:

                        self._nestedControlID._kvData = Utils.Config.getCatalog(
                            self._nestedControlID._catalogName.get(), self._value.get())
                        self._nestedControlID.configure(values=list(self._nestedControlID._kvData.values())) #updated 18.10.2021 daps list

                        _exists = self._nestedControlID.getElementByText(self._nestedControlID._textVariable.get())

                        if _exists is not None:
                            self._nestedControlID._value.set(_exists[0])
                            self._nestedControlID._text.set(_exists[1])
                        else:
                            self._nestedControlID._value.set(list(self._nestedControlID._kvData.keys())[0])#updated 18.10.2021 daps list
                            self._nestedControlID._text.set(list(self._nestedControlID._kvData.values())[0])#updated 18.10.2021 daps list

                        self._nestedControlID._keyVariable.set(self._nestedControlID._value.get())
                        self._nestedControlID._textVariable.set(self._nestedControlID._text.get())
                        self._nestedControlID.configure(textvariable=self._nestedControlID._textVariable)
                        self._nestedControlID.set(self._nestedControlID._textVariable.get())

                        self._nestedControlID.OnSelectedIndexChanged()

                def setVariable(self, refTextVariable):
                    self._textVariable = refTextVariable
                    exists = self.getElementByText(self._textVariable.get())
                    if exists is None:
                        self.resetSelection()
                    else:
                        self.configure(values=list(self._kvData.values()))#updated 18.10.2021 daps list
                        self._value.set(exists[0])
                        self._text.set(exists[1])
                        self._textVariable.set(self._text.get())
                        self.configure(textvariable=self._textVariable)
                        self.set(self._textVariable.get())

                    self.OnSelectedIndexChanged()

                def setVariables(self, refKeyVariable, refTextVariable):
                    self._keyVariable = refKeyVariable
                    self._textVariable = refTextVariable
                    exists = self.getElementByText(self._textVariable.get())
                    if exists is None:
                        self.resetSelection()
                    else:
                        self.configure(values=list(self._kvData.values()))#updated 18.10.2021 daps list
                        self._value.set(exists[0])
                        self._text.set(exists[1])
                        self._keyVariable.set(self._value.get())
                        self._textVariable.set(self._text.get())
                        self.configure(textvariable=self._textVariable)
                        self.set(self._textVariable.get())

                    self.OnSelectedIndexChanged()

                def getElementByText(self, textValue):
                    _outputValue = ""
                    _outputText = ""
                    for _value, _text in self._kvData.items():
                        if _text.strip().lower() == textValue.strip().lower():
                            return _value, _text
                    return None

                def resetSelection(self):
                    self.configure(values=list(self._kvData.values()))#updated 18.10.2021 daps list
                    self._text.set(list(self._kvData.values())[0])#updated 18.10.2021 daps list
                    self._value.set(list(self._kvData.keys())[0])#updated 18.10.2021 daps list
                    self._textVariable.set(list(self._kvData.keys())[0])#updated 18.10.2021 daps list
                    self.configure(textvariable=self._textVariable)
                    self.set(list(self._kvData.values())[list(self._kvData.values()).index(self._text.get())])#updated 18.10.2021 daps list

                def __init__(self, parent, *args, **kwargs):
                    ttk.Combobox.__init__(self, parent)
                    self._kvData = {}
                    self._nestedControlID = None
                    self._keyVariable = tk.StringVar()
                    self._textVariable = tk.StringVar()
                    self._catalogName = tk.StringVar()
                    self._value = tk.StringVar()
                    self._text = tk.StringVar()
                    self._initialValue = tk.StringVar()

                    self._catalogName.set("")
                    self._value.set("")
                    self._text.set("")
                    self._initialValue.set("")

                    self._kvData = kwargs["kvData"]
                    if "nestedControlID" in kwargs:
                        self._nestedControlID = kwargs["nestedControlID"]

                    if "catalogName" in kwargs:
                        self._catalogName.set(str(kwargs["catalogName"]).strip())

                    if "textvariable" in kwargs:
                        self._textVariable = kwargs["textvariable"]
                        self.configure(textvariable=self._textVariable)

                    if "initialValue" in kwargs:
                        self._initialValue.set(str(kwargs["initialValue"]).strip())

                    # sort by Text
                    self._kvData = collections.OrderedDict(sorted(self._kvData.items(), key=lambda x: x[1]))
                    self.configure(values=list(self._kvData.values()))#updated 18.10.2021 daps list
                    self.bind("<<ComboboxSelected>>", self.OnSelectedIndexChanged)

                    if len(self._initialValue.get()) > 0 and getElementByText(self._initialValue.get()) is not None:
                        print("  self._initialValue.get()", self._initialValue.get(), " ->. selectByText ",
                              self._text.get(), itemText, "<<<", getElementByText(self._initialValue.get()), ">>>")

            # end of DropDownList

            class CascadingDropDownList(ttk.Combobox, object):
                def updateList(self):
                    self.configure(values=list(self.kvData.values()))#updated 18.10.2021 daps list
                    self.configure(state=self.state)

                def setValue(self, value):
                    #print("            setValue     ", value)
                    self._defaultValue.set(value)
                    try:
                        self.set(list(self._kvData.values())[list(self._kvData.values()).index(self._defaultValue.get())])#updated 18.10.2021 daps list

                        if self.linkedID != None:
                            try:
                                self.OnSelectionEvent(self.get())
                            except:
                                return

                    except:
                        self.set(list(self._kvData.values())[0])#updated 18.10.2021 daps list
                    return

                def OnSelectionEvent(self, event):
                    _text = self.get()
                    _key = list(self._kvData.keys())[list(self._kvData.values()).index(_text)]#updated 18.10.2021 daps list

                    self._selectedKey.set(_key)
                    self._selectedText.set(_text)
                    if self._linkedID != None:
                        self._linkedID._kvData = Utils.Config.getCatalog(self._linkedID._catalogName.get(), _key)
                        self._linkedID.configure(values=self.list(_linkedID._kvData.values()))#updated 18.10.2021 daps list

                        if self._linkedID._defaultValue.get() == None and \
                                len(self._linkedID._kvData) > 0:
                            self._linkedID.set(list(self._linkedID._kvData.values())[0])#updated 18.10.2021 daps list
                            try:
                                self._linkedID.OnSelectionEvent(list(self._linkedID._kvData.values())[0])#updated 18.10.2021 daps list
                            except:
                                return

                def __init__(self, parent, *args, **kwargs):
                    ttk.Combobox.__init__(self, parent)
                    self._linkedID = None
                    self._catalogName = tk.StringVar()
                    self._loadFromFile = tk.BooleanVar()
                    self._defaultValue = tk.StringVar()
                    self._selectedKey = tk.StringVar()
                    self._selectedText = tk.StringVar()
                    self._state = tk.StringVar()

                    self._linkedID = kwargs["linkedID"]
                    self._catalogName.set(kwargs["catalogName"])
                    self._loadFromFile.set(bool(kwargs["loadFromFile"]))
                    self._defaultValue.set(kwargs["defaultValue"])
                    self._state.set(kwargs["state"])
                    self._selectedText.set("" if self._defaultValue is None else self._defaultValue.get())
                    self._selectedKey.set(self._selectedText)
                    self._kvData = kwargs["kvData"]

                    if self._loadFromFile.get():
                        self._kvData = Utils.Config.getCatalog(self._catalogName.get())
                    else:
                        self._kvData = collections.OrderedDict(sorted(self._kvData.items(), key=lambda x: x[1]))

                    self.configure(values=list(self._kvData.values()))  # , reverse=True))#updated 18.10.2021 daps list
                    self.configure(state=self._state.get())
                    self.bind("<<ComboboxSelected>>", self.OnSelectionEvent)
                    if self._defaultValue.get() == None:
                        self.set(list(self._kvData.values())[0])#updated 18.10.2021 daps list
                    else:
                        try:
                            self.set(list(self._kvData.values())[list(self._kvData.values()).index(self._defaultValue.get())])#updated 18.10.2021 daps list
                        except:
                            self.set(list(self._kvData.values())[0]) #updated 18.10.2021 daps list(self._kvData.values())[0]

                    if self._linkedID != None:
                        try:
                            self.OnSelectionEvent(self.get())
                        except:
                            return

            # end of CascadingDropDownList

            class CollapsibleFrame(tk.Frame, object):
                def __init__(self, parent, text=None, borderwidth=2, width=0, height=16, interior_padx=0,
                             interior_pady=18, background=None, caption_separation=4, caption_font=None,
                             caption_builder=None, icon_x=5, icon_open=None, icon_close=None):
                    tk.Frame.__init__(self, parent)
                    if background is None:
                        background = self.cget("background")

                    self.configure(background=background)

                    self._is_opened = False

                    self._interior_padx = interior_padx
                    self._interior_pady = interior_pady

                    plus_9_0_333333 = "R0lGODlhCQAJAOMLADMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM////////////////////yH5BAEKAA8ALAAAAAAJAAkAQAQb8MlJpVFU6a3pwdXzhSJYIUoxGceRKEjrmU8EADs="
                    minus_9_0_333333 = "R0lGODlhCQAJAOMIADMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM////////////////////////////////yH5BAEKAAgALAAAAAAJAAkAQAQPEMlJ6zQn62O7/12xaWAEADs="

                    self._iconOpen = tk.PhotoImage(data=plus_9_0_333333)
                    self._iconClose = tk.PhotoImage(data=minus_9_0_333333)

                    if icon_open is not None:
                        self._iconOpen = tk.PhotoImage(data=icon_open)
                    if icon_close is not None:
                        self._iconClose = tk.PhotoImage(data=icon_close)

                    height_of_icon = max(self._iconOpen.height(), self._iconClose.height())
                    width_of_icon = max(self._iconOpen.width(), self._iconClose.width())

                    containerFrame_pady = (height_of_icon // 2) + 1

                    self._height = height
                    self._width = width

                    self._containerFrame = tk.Frame(self, borderwidth=1, width=width, height=height, relief=None,
                                                    background=background)
                    self._containerFrame.pack(expand=True, fill='x', pady=(containerFrame_pady, 0))

                    self.interior = tk.Frame(self._containerFrame, background=background)

                    self._headerArea = tk.Frame(self, borderwidth=0, height=20, background="#999999")
                    self._headerArea.place(in_=self._containerFrame, x=icon_x, y=-(height_of_icon // 2), anchor="nw",
                                           bordermode="ignore", relwidth=1.0)

                    _y = (self._headerArea.winfo_reqheight() - height_of_icon) // 2
                    self._collapseButton = tk.Label(self, borderwidth=0, relief='raised', image=self._iconOpen,
                                                    background="#999999")
                    self._collapseButton.place(in_=self._headerArea, x=icon_x, y=_y, anchor="nw", bordermode="ignore")
                    self._collapseButton.bind("<Button-1>", lambda event: self.toggle())

                    if caption_builder is None:
                        self._captionLabel = tk.Label(self, anchor="w", borderwidth=1, text=text,
                                                      background="#999999")  # background="#d9d900",
                        if caption_font is not None:
                            self._captionLabel.configure(font=caption_font)
                    else:
                        self._captionLabel = caption_builder(self)

                        if not isinstance(self._captionLabel, Widget):
                            raise Exception("'caption_builder' doesn't return a tkinter widget")

                    self.after(0, lambda: self._place_caption(caption_separation, icon_x, width_of_icon))

                def update_width(self, width=None):
                    # see
                    # http://wiki.tcl.tk/1255
                    self.after(0, lambda width=width: self._update_width(width))

                def _place_caption(self, caption_separation, icon_x, width_of_icon):
                    self.update()
                    x = caption_separation + icon_x + width_of_icon
                    y = 0

                    self._captionLabel.place(in_=self._headerArea, x=x, y=y, anchor="nw", bordermode="ignore")

                def _update_width(self, width):
                    self.update()
                    if width is None:
                        width = self.interior.winfo_reqwidth()

                    if isinstance(self._interior_pady, (list, tuple)):
                        width += self._interior_pady[0] + self._interior_pady[1]
                    else:
                        width += 2 * self._interior_pady

                    width = max(self._width, width)

                    self._containerFrame.configure(width=width)

                def open(self):
                    self._collapseButton.configure(image=self._iconClose)
                    self._containerFrame.configure(height=self.interior.winfo_reqheight())
                    self.interior.pack(expand=True, fill='x', padx=self._interior_padx, pady=self._interior_pady)
                    self._is_opened = True

                def close(self):
                    self.interior.pack_forget()
                    self._containerFrame.configure(height=self._height)
                    self._collapseButton.configure(image=self._iconOpen)
                    self._is_opened = False

                def toggle(self):
                    if self._is_opened:
                        self.close()
                    else:
                        self.open()

            # end of CollapsibleFrame

            class LstBox(tk.Listbox, object):
                @property
                def value(self):
                    selectedItems = self.curselection()
                    output = []
                    for item in selectedItems:
                        output.append(self.list[int(item)])
                    return output

                @value.setter
                def value(self, values):
                    self.selection_clear(0, 'end')
                    for item in values:
                        for i in range(len(self.list)):
                            if item == self.list[i]:
                                self.selection_set(i)
                                break

                def clearSelection(self):
                    self.selection_clear(0, 'end')
                    self._selectedValues.set("")
                    return

                @property
                def selectedValues(self):
                    return self._selectedValues.get()

                # pass

                @selectedValues.setter
                def selectedValues(self, listOfValues):
                    self.clearSelection()

                    if len(listOfValues) == 0:
                        return

                    _listOfValues = listOfValues.split(',')
                    if len(_listOfValues) == 0:
                        return

                    for item in _listOfValues:
                        for i in range(len(self.list)):
                            if item == self.list[i]:
                                self.selection_set(i)
                                break
                    self.OnSelect()

                def refreshSelection(self):
                    self.selection_clear(0, 'end')
                    if len(self._selectedValues.get()) == 0:
                        return

                    _listOfValues = self._selectedValues.get().split(',')
                    if len(_listOfValues) == 0:
                        return

                    for item in _listOfValues:
                        for i in range(len(self.list)):
                            if item == self.list[i]:
                                self.selection_set(i)
                                break
                    self.OnSelect()

                def OnSelect(self, event=None):
                    selectedItems = self.curselection()
                    lst = []
                    for item in selectedItems:
                        lst.append(self.list[int(item)])
                    self._selectedValues.set(str(','.join(str(x) for x in lst)))

                def __init__(self, master, sortList=False, list={}, *args, **kwargs):
                    tk.Listbox.__init__(self, master, *args, **kwargs)
                    self.bind('<<ListboxSelect>>', self.OnSelect)
                    self._selectedValues = tk.StringVar()
                    self._selectedValues.set("")
                    self.list = []
                    for _key, _value in list.items():
                        self.list.append(_value)

                    self.sortList = sortList

                    if self.sortList:
                        self.list.sort()

                    for item in self.list:
                        self.insert("end", item)

            # end of LstBox

            class AutoScrollContainer(object):
                def __init__(self, master):
                    # try:
                    vsb = tk.Scrollbar(master, orient='vertical', command=self.yview)
                    # except:
                    # 	pass
                    hsb = tk.Scrollbar(master, orient='horizontal', command=self.xview)

                    # try:
                    self.configure(yscrollcommand=self.OnAutoscroll(vsb))
                    # except:
                    # 	pass
                    self.configure(xscrollcommand=self.OnAutoscroll(hsb))

                    self.grid(column=0, row=0, sticky='nsew')
                    # try:
                    vsb.grid(column=1, row=0, sticky='ns')
                    # except:
                    # 	pass
                    hsb.grid(column=0, row=1, sticky='we')

                    master.grid_columnconfigure(0, weight=1)
                    master.grid_rowconfigure(0, weight=1)

                    # Copy geometry methods of master (taken from ScrolledText.py)
                    try:
                        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() | tk.Place.__dict__.keys()
                    except:
                        methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() + tk.Place.__dict__.keys()

                    for meth in methods:
                        if meth[0] != '_' and meth not in ('config', 'configure'):
                            setattr(self, meth, getattr(master, meth))

                @staticmethod
                def OnAutoscroll(scrollbar):
                    '''Hide and show scrollbar as needed.'''

                    def wrapped(first, last):
                        first, last = float(first), float(last)
                        if first <= 0 and last >= 1:
                            scrollbar.grid_remove()
                        else:
                            scrollbar.grid()
                        scrollbar.set(first, last)

                    return wrapped

            # end of AutoScrollContainer

            class ScrolledTreeView(AutoScrollContainer, ttk.Treeview):
                def clearOnMove(self, event=None):
                    try:
                        if self.last_focus:
                            self.item(self.last_focus, tags=["normal"])
                            # self.setTooTipStyle(self.last_focus, ["normal", "focus"], "normal")
                            self.hideTip()

                            self.last_focus = None
                            self.tipwindow = None
                            self.id = None
                            self.x = self.y = 0
                    except:
                        pass

                def OnMotion(self, event):
                    _iid = self.identify_row(event.y)

                    if _iid != self.last_focus:
                        if self.last_focus:
                            self.item(self.last_focus, tags=["normal"])
                            self.hideTip()
                        self.item(_iid, tags=["focus"])
                        self.last_focus = _iid
                        if len(self.item(_iid)["values"]) != 3:
                            return
                        self.showTip(_iid, self.item(_iid)["values"][2], event.x, event.y)

                def showTip(self, itemId, text, event_x, event_y):
                    "Display text in tooltip window"
                    self.text = text
                    if self.tipwindow or not self.text:
                        return
                    # x, y, cx, cy = self.bbox(itemId)
                    x = 0
                    y = 0
                    cx = event_x
                    cy = event_y
                    x = x + self.winfo_rootx() + 20
                    y = y + cy + self.winfo_rooty() + 20
                    self.tipwindow = tw = tk.Toplevel(self)
                    tw.wm_overrideredirect(1)
                    tw.wm_geometry("+%d+%d" % (x, y))
                    try:
                        # For Mac OS
                        tw.tk.call("::tk::unsupported::MacWindowStyle",
                                   "style", tw._w,
                                   "help", "noActivates")
                    except tk.TclError:
                        pass

                    label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                                     background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                                     font=("tahoma", "8", "normal"))
                    label.pack(ipadx=1)

                def hideTip(self, event=None):
                    if not self.showToolTip:
                        return

                    try:
                        tw = self.tipwindow
                        self.tipwindow = None
                        if tw:
                            tw.destroy()
                    except:
                        pass

                def __init__(self, master, **kw):
                    self.showToolTip = False
                    self.tipwindow = None
                    self.id = None
                    self.x = self.y = 0

                    if "showToolTip" in kw:
                        self.showToolTip = bool(kw["showToolTip"])
                        del kw["showToolTip"]
                    self.container = tk.Frame(master)
                    ttk.Treeview.__init__(self, self.container, **kw)
                    Utils.UI.Controls.AutoScrollContainer.__init__(self, self.container)
                    if self.showToolTip:
                        self.last_focus = None
                        self.tag_configure('normal', font=("tahoma", "7", "normal"))
                        self.tag_configure('focus', background="#ffff00", font=("tahoma", "6", "normal"))
                        self.bind("<Motion>", self.OnMotion)
                        self.bind("<Leave>", self.clearOnMove)

            # end of ScrolledTreeView

            class ScrollableContainer(tk.Frame, object):
                def __init__(self, parent, width=None, anchor="n", height=None, background=None, inner_frame=tk.Frame,
                             **kw):
                    tk.Frame.__init__(self, parent, class_="ScrollableContainer", background=background)

                    self.grid_columnconfigure(0, weight=1)
                    self.grid_rowconfigure(0, weight=1)

                    self._width = width
                    self._height = height

                    self.canvas = tk.Canvas(self, background=background, highlightthickness=0, width=width,
                                            height=height)  # background
                    self.canvas.grid(row=0, column=0, sticky='news')

                    self.yscrollbar = tk.Scrollbar(self, orient='vertical')
                    self.yscrollbar.grid(row=0, column=1, sticky='ns')
                    self.canvas.configure(yscrollcommand=self.yscrollbar.set)
                    self.yscrollbar['command'] = self.canvas.yview

                    self.xscrollbar = tk.Scrollbar(self, orient='horizontal')
                    self.xscrollbar.grid(row=1, column=0, sticky='ew')
                    self.canvas.configure(xscrollcommand=self.xscrollbar.set)
                    self.xscrollbar['command'] = self.canvas.xview

                    self.rowconfigure(0, weight=1)
                    self.columnconfigure(0, weight=1)

                    self.innerframe = inner_frame(self.canvas, **kw)
                    self.innerframe.pack(anchor=anchor)

                    self.canvas.create_window(0, 0, window=self.innerframe, anchor='nw', tags="inner_frame")
                    self.canvas.bind('<Configure>', self.OnCanvas_Configure)

                @property
                def width(self):
                    return self.canvas.winfo_width()

                @property
                def height(self):
                    return self.canvas.winfo_height()

                def setSize(self, width, height):
                    self.canvas.configure(width=width, height=height)

                def OnCanvas_Configure(self, event):
                    width = max(self.innerframe.winfo_reqwidth(), event.width)
                    height = max(self.innerframe.winfo_reqheight(), event.height)

                    self.canvas.configure(scrollregion="0 0 %s %s" % (width, height))
                    self.canvas.itemconfigure("inner_frame", width=width, height=height)
                    return

                def updateViewPort(self, newWidth=None, newHeight=None):
                    self.update()

                    if newWidth is None:
                        window_width = self.innerframe.winfo_reqwidth()
                        if self._width is None:
                            canvas_width = window_width
                        else:
                            canvas_width = min(self._width, window_width)
                    else:
                        canvas_width = newWidth
                        window_width = canvas_width

                    if newHeight is None:
                        window_height = self.innerframe.winfo_reqheight()
                        if self._height is None:
                            canvas_height = window_height
                        else:
                            canvas_height = min(self._height, window_height)
                    else:
                        canvas_height = newHeight
                        window_height = canvas_height

                    self.canvas.configure(scrollregion="0 0 %s %s" % (window_width, window_height), width=canvas_width,
                                          height=canvas_height)
                    self.canvas.itemconfigure("inner_frame", width=window_width, height=window_height)
                    return
        # end of ScrollableContainer

    class Resources:
        @staticmethod
        class Icons:
            align_justify_16_0_333333 = "R0lGODlhEAAQALMJAEBAQFZWVlNTU1hYWEFBQVVVVf39/fr6+jMzM////wAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAkALAAAAAAQABAAAAQ1MMlJazIn670NQWAoikQwnmFgrVOBooXwngLLDvM4ALkIYJxgxgAUcgy8HghgUiJUtqg0EQEAOw=="
            building_o_16_0_333333 = "R0lGODlhEAAQAMQSAPr6+lVVVfj4+PX19XJycklJSYGBgXNzc1NTU/n5+Tg4OE9PT0NDQ0FBQVFRUfv7+/39/TMzM////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAABIALAAAAAAQABAAAAVYoIREZGk2kKRGAOS+7/KoUgQFEm4kueTMqxRt6APWIAxJ8iBQFmk24vAHFUqfwYZES2gmqcGrCnzUcr3Yozht0z4AANXXGK2RBjRyvYQfGwsmgREKVmtSIQA7"
            cube_16_0_333333 = "R0lGODlhEAAQANU6APr6+jg4OExMTIGBgTY2Njk5Off399TU1NLS0oiIiMTExI2NjaysrGFhYWNjY3t7e/Hx8bGxsXV1dVZWVsbGxm5ubvv7+/X19eLi4tPT09DQ0L+/v+np6UFBQdXV1fj4+OTk5HZ2dsnJycXFxXJycnFxcbu7u5SUlE1NTdnZ2d3d3UBAQDU1NXd3d5eXl+7u7sPDw4mJieXl5fb29kdHR1VVVfn5+f39/czMzDMzM////wAAAAAAAAAAAAAAAAAAACH5BAEAADoALAAAAAAQABAAAAaBQJ1QaFM0GiPbcHnLSAInUGqQCx1uQsiC0PJghxYNibCACB6fpVpnGAhyucnGsL6YagW4PldC3GwUDgUuMjN7hywJKl8Ah3siao2OcDiRk5SWl5VLNjkxk5tCGA4JOgcoh5scFQIISwodejgvDyswazo3EQE5NAERX7g6NgwMSmpBADs="
            file_o_16_0_333333 = "R0lGODlhEAAQALMNAPr6+kNDQ2lpacjIyJ6enrm5uba2tnl5eU1NTczMzJ+fn/39/TMzM////wAAAAAAACH5BAEAAA0ALAAAAAAQABAAAAREsB1GKwul6c3A+h/ADMqmMYvZLEyTECaqstpgcKmKVAGuaqHWKfdbCRuyotGnpA2Vy2fzmCw6kcTftao9CixgigAKjQAAOw=="
            folder_16_0_d4be2b = "R0lGODlhEAAQAIQWANS+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K////////////////////////////////////////yH5BAEKAB8ALAAAAAAQABAAQAU04CeOZPlVaKquz4pOUhxHomujzqky5njbjZ/r8YEIKxReb/mZuJhHlS5aaVGr16qRylyGAAA7"
            folder_o_16_0_d4be2b = "R0lGODlhEAAQAIQYANS+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K////////////////////////////////yH5BAEKAB8ALAAAAAAQABAAQAUy4CeOZPldZnqiJHW9sNWcqolWcU3r48v3nwhsSIT8SpMSK7XkOZo631H6u0iOnwdWFAIAOw=="
            folder_open_16_0_d4be2b = "R0lGODlhEAAQAKUlANS+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K////////////////////////////////////////////////////////////////////////////////////////////////////////////yH5BAEKAD8ALAAAAAAQABAAAAY9wJ9wSCwaj8URaXlBCj/LqPMXrVY3RKuWZBlurRrvEjQVLj1ls0jI+S6pwo6bRBli5pmsGz0UfUMVaYJlQQA7"
            folder_open_o_16_0_d4be2b = "R0lGODlhEAAQAKUmANS+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K9S+K////////////////////////////////////////////////////////////////////////////////////////////////////////yH5BAEKAD8ALAAAAAAQABAAQAY/wJ9wSCz+SkNMaclkko5EZfNC1BiLFCKIwwldicivcDREdsTCDHrN/hBF6LC4Ul7Lw5y1puRZW4YbTYJ5bFdBADs="
            folder_open_o_16_0_333333 = "R0lGODlhEAAQANUjAFFRUfv7+2VlZVVVVenp6dLS0u3t7fb29ujo6Hp6eqysrPDw8HZ2durq6klJSVZWVmlpaefn57S0tDg4OExMTD09Pa2trUBAQMbGxjU1NcLCwk9PT+7u7vz8/Pj4+PLy8jY2Nv39/TMzM////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAACMALAAAAAAQABAAAAZewJFwSCwKQ4FAyFgsXACAioY5dHiEnQlVKFoKBaJwWHAYdrcRhtnLDIHW24AI3gCL76KMomsAGLYLAyIcGx9xDwQiFAhbIRAFIwMWIZSVlQcJEkIEAHh3ABhboqNFQQA7"
            folder_open_o_16_0_bfa600 = "R0lGODlhEAAQAKUmAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAL+mAP///////////////////////////////////////////////////////////////////////////////////////////////////////yH5BAEKAD8ALAAAAAAQABAAAAY/wJ9wSCwaj0UQhxNCDj9EkfNXImJKWOyFWJ1Whl3nCDylkoXXrLpEMv84ZU21U85QPWWLUFOmEDdranBlhIRBADs="
            info_circle_16_0_00aa00 = "R0lGODlhEAAQAKUyAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAP///////////////////////////////////////////////////////yH5BAEKAD8ALAAAAAAQABAAQAZSwJ9wOHKdPsPhKsZkDptNIXQKRQpNzmQqOyxFpd+fCpqkgrlCUROUHJJcKGtb2GGGwKy2h3yOvYQbfH1OMFNPhoGCZj8gYUIcTH9JdVQtc5eXQQA7"
            save_16_0_333333 = "R0lGODlhEAAQAMQaANjY2EFBQfX19fz8/G9vb0NDQ8HBwWBgYJGRkbGxsdDQ0FxcXGpqasTExGFhYWVlZfn5+eXl5Tg4OLCwsGlpaaCgoG1tbf39/fr6+jMzM////wAAAAAAAAAAAAAAAAAAACH5BAEAABoALAAAAAAQABAAAAVgIJONJBk0WqplAkVecBY9k5phFmljg5Okt9xopxkcDCucDohJQSRJRGlUuOxuGox2q2Jiu2BvUwMrw66YyrRESAYV5rIg48YBwln6LXgPY/R/dnh/SQtrhwFWW4uMGFYhADs="

            th_large_16_0_333333 = "R0lGODlhEAAQALMMAKWlpfDw8FNTU2dnZ2lpaZGRkZSUlFVVVTU1Ne/v7/39/TMzM////wAAAAAAAAAAACH5BAEAAAwALAAAAAAQABAAAAREkMlJ61RY0axZWSAoYEIIfiaYJGkbrq4Lt0gbBDRQhwNGmAiAhLPJSAypA+aQQrZmMRM0qmLRbLhUcAfqKX6hoGU8iQAAOw=="
            user_o_16_0_333333 = "R0lGODlhEAAQANUrAPDw8Pz8/Glpaf39/e/v7zg4OMHBwTs7O2dnZ0VFRc7Ozs3NzTk5OT4+PmBgYPPz84SEhEdHR4aGhuLi4tra2qioqLi4uJmZmZeXl8jIyK2trU9PT/X19UBAQO3t7WpqapWVlYiIiPn5+dbW1snJybGxsT09PYWFhVFRUYODgzMzM////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAACsALAAAAAAQABAAAAZxwJVQuECYBIqhcnhKEQKEVGg5XKSWqSRVAFgSPtRVI7AMNMKIrpIgCGcgWBJ1EilAAAFAqpCgKDkRXQYODA4GKw8bHkMVh2ErIxJDAg+PKwMHQwlklgUDQigilisMQxYYn2ElIEoaHSqwsSoHF6mjVEEAOw=="

            chevron_circle_up_16_0_333333 = "R0lGODlhEAAQAKU8ADMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM////////////////yH5BAEKAD8ALAAAAAAQABAAAAZfwJ9QqMrtdrGhknhsHm/LH8xJ3SlTTijKqRtmhybn6idqQpUl5+91tEV/pOYPt6uhlaPjT2YdnnY4SnpxM0JbR4FCej9PU1wuRy1CLFVVSjSVckstmW9CMU06J56kSkEAOw=="
            chevron_circle_down_16_0_333333 = "R0lGODlhEAAQAKU6ADMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM////////////////////////yH5BAEKAD8ALAAAAAAQABAAAAZawJ9QiLrlcrChknhsHmvL38tJzSlNVSpu2DRSvanfKHcTspzC0/Hnsg5Xa67VlospVct17GiP/po/JE0yUWh/TTNKTi1mTomHgEM0WZFKLZR+QjBNOCWZn0pBADs="
            angle_double_up_16_0_333333 = "R0lGODlhEAAQAKUqADMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM////////////////////////////////////////////////////////////////////////////////////////yH5BAEKAD8ALAAAAAAQABAAQAZcwJ9wSCwKP8NSCpU6DTvFSio05KQyxVEqYvw5UqauJUXGGikp0FDyTGGKpNRk+A137/jfWJP/SalWZkVoakQdbkMPaUlNQx4pF3ByXo1GcWxEdUMbKRB4XyJ9RkEAOw=="
            angle_double_down_16_0_333333 = "R0lGODlhEAAQAKUnADMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM////////////////////////////////////////////////////////////////////////////////////////////////////yH5BAEKAD8ALAAAAAAQABAAQAZNwJ9wSCwKTaRhxsQZjkzEpaj4YRqPpd/TiDGFrkKQaVOU/jzWK7K4BR/dX/cPpPReq82oaSrEEzVJQksmaVodQ2tGbUWJWlByhI9yk0EAOw=="
            angle_up_16_0_333333 = "R0lGODlhEAAQAIQWADMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM////////////////////////////////////////yH5BAEKAB8ALAAAAAAQABAAQAUy4CeOZDlGlVMu1WSe7SvP9Iw+nxKTUNXMjIqkRiwaSSjK7oVSiVguZOoFHSVqiKN2FAIAOw=="
            angle_down_16_0_333333 = "R0lGODlhEAAQAIQSADMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM////////////////////////////////////////////////////////yH5BAEKAB8ALAAAAAAQABAAQAUp4CeOZFlG0PhEZmqST/POdP2h70pHvO3/QBNupiMNVawZzpG0NYNQUwgAOw=="

            child_16_0_333333 = "R0lGODlhEAAQAKUnADMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM////////////////////////////////////////////////////////////////////////////////////////////////////yH5BAEKAD8ALAAAAAAQABAAQAY3wJ9wSCwaf6ak6Tg0jYqmDxO5XE6FHuVVqDSFtt0tsoQUU0lTk4hrQpeP3SToGgZr7W961TwNAgA7"
            child_16_0_00aa00 = "R0lGODlhEAAQAKUnAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAACqAP///////////////////////////////////////////////////////////////////////////////////////////////////yH5BAEKAD8ALAAAAAAQABAAQAY3wJ9wSCwaf6ak6Tg0jYqmDxO5XE6FHuVVqDSFtt0tsoQUU0lTk4hrQpeP3SToGgZr7W961TwNAgA7"

            plus_9_0_333333 = "R0lGODlhCQAJAOMLADMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM////////////////////yH5BAEKAA8ALAAAAAAJAAkAQAQb8MlJpVFU6a3pwdXzhSJYIUoxGceRKEjrmU8EADs="
            minus_9_0_333333 = "R0lGODlhCQAJAOMIADMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM////////////////////////////////yH5BAEKAAgALAAAAAAJAAkAQAQPEMlJ6zQn62O7/12xaWAEADs="
            plus_square_o_16_0_333333 = "R0lGODlhEAAQAIQaADMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM////////////////////////yH5BAEKAB8ALAAAAAAQABAAQAVF4CeOZPllY6RWlRqJKFqqZWzeMnWX12nSJNvsFRRhdiOKRCTJOJ/QTO9jQRZlJOBI+HGxXDDfsCbOErefiRUtmkShVVEIADs="
            minus_square_o_16_0_333333 = "R0lGODlhEAAQAIQZADMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM////////////////////////////yH5BAEKAB8ALAAAAAAQABAAQAU34CeOZPlhYoWt7EqdsGmiqFzWkk1asS7SvlHtEpRARJCWcsX7TIK/ng8IpQat008E2ossWU9RCAA7"

            gears_16_0_333333 = "R0lGODdhEAAQAIcAMf///zMzMzs7O+Hh4fHx8c3NzcvLy2VlZWNjY6ysrFxcXOLi4llZWd3d3UlJSczMzOjo6MHBwUVFRd7e3rCwsHd3d5qamnp6eo2NjaWlpZKSkpWVlTk5Ofb29p6enp+fn5mZmaCgoKOjo6ampoGBgX9/f6mpqa+vr3JycnFxcbGxsbOzs2FhYV9fX11dXfX19VpaWuPj40xMTPz8/OXl5UdHR+rq6kNDQzg4OPT09EBAQJ2dnT09Pf39/T4+Pj8/Pzo6OkFBQUJCQjc3N0RERDY2NkZGRjU1NUhISDQ0NEpKSktLSzIyMk1NTU5OTk9PT1BQUFFRUVJSUlNTU1RUVFVVVVZWVldXV1hYWDExMTAwMFtbWy8vLy4uLl5eXi0tLWBgYCwsLGJiYisrK2RkZCoqKmZmZmdnZ2hoaGlpaWpqamtra2xsbG1tbW5ubm9vb3BwcCkpKSgoKHNzc3R0dHV1dXZ2dicnJ3h4eHl5eSYmJnt7e3x8fH19fX5+fiUlJYCAgCQkJIKCgoODg4SEhIWFhYaGhoeHh4iIiImJiYqKiouLi4yMjCMjI46Ojo+Pj5CQkJGRkSIiIpOTk5SUlCEhIZaWlpeXl5iYmCAgIB8fH5ubm5ycnB4eHh0dHRwcHBsbG6GhoaKiohoaGqSkpBkZGRgYGKenp6ioqBcXF6qqqqurqxYWFq2tra6urhUVFRQUFBMTE7KyshISErS0tLW1tba2tre3t7i4uLm5ubq6uru7u7y8vL29vb6+vr+/v8DAwBEREcLCwsPDw8TExMXFxcbGxsfHx8jIyMnJycrKyhAQEA8PDw4ODs7Ozs/Pz9DQ0NHR0dLS0tPT09TU1NXV1dbW1tfX19jY2NnZ2dra2tvb29zc3A0NDQwMDN/f3+Dg4AsLCwoKCgkJCeTk5AgICObm5ufn5wcHB+np6QYGBuvr6+zs7O3t7e7u7u/v7/Dw8AUFBfLy8vPz8wQEBAMDAwICAvf39/j4+Pn5+fr6+vv7+wEBATw8PP7+/gAAACH5BAEAAAAALAAAAAAQABAARwitAAEIHEiwIIAACAkMJIAwgEEaCgYcCHBgQMQUHHp04IACAAQYEyYiGMCgQQUBM14IqGCwIAaEGwQOCCDgAQEDAgLEAHAhQoISAhcE4FGAQIGcC3j6JNHSJcymBHdMMCCi4AocFAZmcJADgowMABg0HHsAgAYHNywAMKEgQIGBBgIgOFFQBQu3Ax8EcDHCIIKxDVuYlaBDLUEKARIM9CChg40aH6AKBNHAQAgAAQEAOw=="

        #  "R0lGODlhEAAQAIcAMf///zMzMzs7O+Hh4fHx8c3NzcvLy2VlZWNjY6ysrFxcXOLi4llZWd3d3UlJSczMzOjo6MHBwUVFRd7e3rCwsHd3d5qamnp6eo2NjaWlpZKSkpWVlTk5Ofb29p6enp+fn5mZmaCgoKOjo6ampoGBgX9/f6mpqa+vr3JycnFxcbGxsbOzs2FhYV9fX11dXfX19VpaWuPj40xMTPz8/OXl5UdHR+rq6kNDQzg4OPT09EBAQJ2dnT09Pf39/T4+Pj8/Pzo6OkFBQUJCQjc3N0RERDY2NkZGRjU1NUhISDQ0NEpKSktLSzIyMk1NTU5OTk9PT1BQUFFRUVJSUlNTU1RUVFVVVVZWVldXV1hYWDExMTAwMFtbWy8vLy4uLl5eXi0tLWBgYCwsLGJiYisrK2RkZCoqKmZmZmdnZ2hoaGlpaWpqamtra2xsbG1tbW5ubm9vb3BwcCkpKSgoKHNzc3R0dHV1dXZ2dicnJ3h4eHl5eSYmJnt7e3x8fH19fX5+fiUlJYCAgCQkJIKCgoODg4SEhIWFhYaGhoeHh4iIiImJiYqKiouLi4yMjCMjI46Ojo+Pj5CQkJGRkSIiIpOTk5SUlCEhIZaWlpeXl5iYmCAgIB8fH5ubm5ycnB4eHh0dHRwcHBsbG6GhoaKiohoaGqSkpBkZGRgYGKenp6ioqBcXF6qqqqurqxYWFq2tra6urhUVFRQUFBMTE7KyshISErS0tLW1tba2tre3t7i4uLm5ubq6uru7u7y8vL29vb6+vr+/v8DAwBEREcLCwsPDw8TExMXFxcbGxsfHx8jIyMnJycrKyhAQEA8PDw4ODs7Ozs/Pz9DQ0NHR0dLS0tPT09TU1NXV1dbW1tfX19jY2NnZ2dra2tvb29zc3A0NDQwMDN/f3+Dg4AsLCwoKCgkJCeTk5AgICObm5ufn5wcHB+np6QYGBuvr6+zs7O3t7e7u7u/v7/Dw8AUFBfLy8vPz8wQEBAMDAwICAvf39/j4+Pn5+fr6+vv7+wEBATw8PP7+/gAAACwAAAAAEAAQAAcIrgABCBxIsKBBgzsmGBBxsCCGAAE2FFyBg8LADA5yQJCRAQANBQMOBDgwAGQKDj06cEABgAHElxAPANDg4IYFgQMCCHhAwICAADEAXIiQoAQAEwoCFBhoIACCEwVfEhhI4GVBFSyUDnwQwMUIgwsC8ChAoMDPBUKJkhCIAObLFjMl6LgJAAKMCSIRDGDQoIKAGS8EVCBIIUCCgR4kdLBR40PDgQ8jPh4IooGBEAACAgA7"
        #   ="R0lGODlhEAAQAOcqAAAAAAEBAQICAgMDAwQEBAUFBQYGBgcHBwgICAkJCQoKCgsLCwwMDA0NDQ4ODg8PDxAQEBERERISEhMTExQUFBUVFRYWFhcXFxgYGBkZGRoaGhsbGxwcHB0dHR4eHh8fHyAgICEhISIiIiMjIyQkJCUlJSYmJicnJygoKCkpKSoqKisrKywsLC0tLS4uLi8vLzAwMDExMTIyMjMzMzQ0NDU1NTY2Njc3Nzg4ODk5OTo6Ojs7Ozw8PD09PT4+Pj8/P0BAQEFBQUJCQkNDQ0REREVFRUZGRkdHR0hISElJSUpKSktLS0xMTE1NTU5OTk9PT1BQUFFRUVJSUlNTU1RUVFVVVVZWVldXV1hYWFlZWVpaWltbW1xcXF1dXV5eXl9fX2BgYGFhYWJiYmNjY2RkZGVlZWZmZmdnZ2hoaGlpaWpqamtra2xsbG1tbW5ubm9vb3BwcHFxcXJycnNzc3R0dHV1dXZ2dnd3d3h4eHl5eXp6ent7e3x8fH19fX5+fn9/f4CAgIGBgYKCgoODg4SEhIWFhYaGhoeHh4iIiImJiYqKiouLi4yMjI2NjY6Ojo+Pj5CQkJGRkZKSkpOTk5SUlJWVlZaWlpeXl5iYmJmZmZqampubm5ycnJ2dnZ6enp+fn6CgoKGhoaKioqOjo6SkpKWlpaampqenp6ioqKmpqaqqqqurq6ysrK2tra6urq+vr7CwsLGxsbKysrOzs7S0tLW1tba2tre3t7i4uLm5ubq6uru7u7y8vL29vb6+vr+/v8DAwMHBwcLCwsPDw8TExMXFxcbGxsfHx8jIyMnJycrKysvLy8zMzM3Nzc7Ozs/Pz9DQ0NHR0dLS0tPT09TU1NXV1dbW1tfX19jY2NnZ2dra2tvb29zc3N3d3d7e3t/f3+Dg4OHh4eLi4uPj4+Tk5OXl5ebm5ufn5+jo6Onp6erq6uvr6+zs7O3t7e7u7u/v7/Dw8PHx8fLy8vPz8/T09PX19fb29vf39/j4+Pn5+fr6+vv7+/z8/P39/f7+/v///yH5BAEKAP8ALAAAAAAQABAAAAhKAP8JHEiwoMGDCA/OWDjDYEOCDx/+a8hw4sSIFBlqzCjx4sCFAiOG7OixYEWIIE2STOlQYkqRFzeCPBkypsWXK03WTDiSJU+CAQEAOw=="
        #
