import uuid
import sys
#import ConfigParser updated on 18.10.2021 daps
import os

if sys.version_info[0] == 3:
    from xml.etree import ElementTree
    import configparser as ConfigParser # updated on 18.10.2021 daps
    import operator as operator
else:
    from xml.etree import cElementTree as ElementTree
    import ConfigParser  # updated on 18.10.2021 daps

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Utils"))
from CUtils import *

class Simulation(object):

    # building
    class Building(object):
        def getKey(self):
            return self.id

        # building zone
        class Zone(object):
            # constructor
            def __init__(self, id=0, name="Undefined", activities="", isGroundFloor=False, windowCount=0, floorArea=0):
                # set initial values
                self.id = id
                self.name = name
                self.activities = activities
                self.isGroundFloor = isGroundFloor
                self.windowCount = windowCount
                self.floorArea = floorArea
                self.varName = ""

            def __repr__(self):
                return '{}: {} {} {} {} {} {} {}'.format(self.__class__.__name__,
                    self.id,
                    self.name,
                    self.activities,
                    self.isGroundFloor,
                    self.windowCount,
                    self.floorArea,
                    self.varName
                    )

        class Occupant(object):
            class Profile(object):
                # constructor
                def __init__(self):
                    self.ID = str(uuid.uuid4()) # Utils.Constants.emptyGUID
                    self.template = "Auto_Generate"
                    # set initial values
                    self.monday = [0.021,0.021,0.021,0.021,0.021,0.021,0.021,0.025,0.250,0.422,0.309,0.377,0.187,0.375,0.426,0.396,0.375,0.432,0.084,0.070,0.047,0.039,0.038,0.038]
                    self.tuesday = [0.040,0.038,0.038,0.038,0.038,0.038,0.038,0.046,0.320,0.401,0.325,0.417,0.196,0.372,0.435,0.402,0.334,0.435,0.100,0.053,0.044,0.044,0.042,0.042]
                    self.wednesday = [0.041,0.041,0.041,0.041,0.041,0.041,0.041,0.062,0.342,0.403,0.297,0.342,0.194,0.354,0.395,0.363,0.336,0.383,0.080,0.043,0.027,0.026,0.026,0.026]
                    self.thursday = [0.024,0.024,0.024,0.024,0.024,0.024,0.024,0.029,0.265,0.373,0.271,0.368,0.193,0.361,0.402,0.357,0.324,0.367,0.094,0.067,0.032,0.032,0.030,0.030]
                    self.friday = [0.030,0.029,0.029,0.029,0.029,0.029,0.029,0.055,0.327,0.367,0.304,0.373,0.215,0.317,0.280,0.239,0.197,0.125,0.066,0.069,0.031,0.029,0.027,0.027]
                    self.saturday = [0.028,0.030,0.029,0.029,0.030,0.029,0.029,0.030,0.030,0.030,0.035,0.037,0.030,0.032,0.041,0.045,0.042,0.034,0.035,0.032,0.027,0.024,0.021,0.021]
                    self.sunday = [0.021,0.021,0.021,0.021,0.021,0.021,0.021,0.021,0.024,0.025,0.032,0.045,0.040,0.041,0.033,0.032,0.033,0.031,0.031,0.028,0.026,0.027,0.025,0.025]
                    
                    self.p0 = [0.919825741,0.013844725,0.011501807,0.001339251,0.002836063,0.000551457,0.00416508,0.002205826,0.001921411,0.041808638]
                    self.p1 = [0.939100335,0.006994969,0.009801527,0.00138011,0.000649464,0.000378854,0.001493399,0.000852422,0.005975069,0.033373851]
                    self.p2 = [0.917089915,0.006584197,0.009081158,0.000648414,0.000419561,0.000355992,0.000992734,0.000533987,0.001857737,0.062436305]
                    self.p3 = [0.951153488,0.005358711,0.007391091,0.00066914,0.000216487,0.000275529,0.000670157,0.000367372,0.001530099,0.032367926]
                    self.p4 = [0.937065664,0.002301296,0.006442035,0.000482765,0.000311292,5.61E-05,0.003180351,0.000299654,0.006490885,0.043369963]
                    self.p5 = [0.786321891,0.004354631,0.004626809,0.000413308,3.74E-05,2.74E-05,-0.00295183,0.000102617,0.015271177,0.191796565]
                    self.p6 = [0.026403697,0.264805246,0.01058878,0.000382654,0.002841571,1.30E-05,0.467817507,4.93E-05,0.027870405,0.199227893]
                    self.p7 = [0.00988392,0.239469081,0.079181036,0.000283675,0.039296265,0.014713453,0.28130066,0.000150597,0.03901277,0.296708542]
                    self.p8 = [0.005733916,0.202435209,0.097657554,0.000512011,0.051674885,0.020714453,0.218457976,0.00483924,0.063424244,0.334550512]
                    self.p9 = [0.003974416,0.196610979,0.097974053,0.000907322,0.051264585,0.034354387,0.182244082,0.006284721,0.083621872,0.342763584]
                    self.p10 = [0.002335063,0.128891935,0.080001785,0.000602573,0.053281638,0.059040355,0.136516178,0.00817024,0.063238793,0.467921441]
                    self.p11 = [0.002297845,0.161057949,0.081886738,0.000428288,0.045818825,0.040169253,0.112419987,0.009160281,0.050551547,0.496209287]
                    self.p12 = [0.002284592,0.133397506,0.103489838,0.000341735,0.089588269,0.019784265,0.080821155,0.010819317,0.046447074,0.513026249]
                    self.p13 = [0.003689056,0.125892986,0.128342238,0.000246571,0.060598163,0.029735183,0.072343993,0.01041524,0.057880359,0.510856211]
                    self.p14 = [0.006881885,0.137211242,0.154726069,0.000150362,0.052593445,0.012949243,0.05941406,0.014348063,0.055448334,0.506277298]
                    self.p15 = [0.007597511,0.165290607,0.166569433,8.52E-05,0.060986828,0.007499695,0.049445514,0.011688156,0.037899725,0.492937353]
                    self.p16 = [0.006089774,0.190880161,0.157068349,0.000448044,0.090650666,0.015137081,0.030782018,0.013370052,0.057158892,0.438414964]
                    self.p17 = [0.004529342,0.259295578,0.137986247,7.16E-05,0.11355052,0.003086002,0.021481626,0.004022928,0.050798189,0.405177922]
                    self.p18 = [0.003553815,0.263509191,0.229487618,0.003571083,0.032872487,0.006196116,0.021207565,0.000769058,0.06979575,0.369037317]
                    self.p19 = [0.002921876,0.281412147,0.245210312,0.000475462,0.026663102,0.001157612,0.028112032,0.00026018,0.05242258,0.361364696]
                    self.p20 = [0.008918376,0.325072665,0.339974397,0.000522971,0.053429758,0.003801955,0.050574538,0.003411859,0.053440375,0.160853107]
                    self.p21 = [0.058472472,0.35872563,0.303962096,0.001002144,0.026996622,0.009391164,0.060013714,0.007363827,0.038445311,0.13562702]
                    self.p22 = [0.291331879,0.255574037,0.171644968,0.000809695,0.01262497,0.007688428,0.055741103,0.00519364,0.0324231,0.166968182]
                    self.p23 = [0.483270594,0.155393009,0.12765826,0.000555775,0.006987987,0.002669004,0.037070308,0.001744559,0.018725401,0.165925102]

            def __init__(self, id=0, name='', description='', categoryID='', category='', regionID='', region='', sectorID='', sector='', zoneId='', zone='', power=0, windowId='', window='', shadeId='', shade='', activityId='', sex='', familyID='', educationID='', ageGroup='', ownComputer=False, isRetired=False, isMarried=False, isUnEmployed=False):
                self.uuid = str(uuid.uuid4())
                self.id = id
                self.name = name
                self.description = description
                self.categoryID = categoryID
                self.category = category
                self.regionID = regionID
                self.region = region
                self.sectorID = sectorID
                self.sector = sector
                self.zoneId = zoneId
                self.zone = zone
                self.power = power
                self.windowId = windowId
                self.window = window
                self.shadeId = shadeId
                self.shade = shade
                self.activityId = activityId
                self.sex = sex
                self.familyID = familyID
                self.educationID = educationID
                self.ageGroup = ageGroup
                self.ownComputer = ownComputer
                self.isRetired = isRetired
                self.isMarried = isMarried
                self.isUnEmployed = isUnEmployed

                self.profile = Simulation.Building.Occupant.Profile()
                self.profile.template = self.activityId

        def clearZones(self):
            del self.zones[:]

        def clearOccupants(self):
            del self.occupants[:]

        def getZoneByName(self, zoneName):
            for i in range(len(self.zones)):
                if self.zones[i].name.strip().lower() == zoneName.strip().lower():
                    return self.zones[i]
            return None

        # constructor
        def __init__(self, id=0, name="", zones=None, occupants=None):
            self.id = id
            self.name = name
            # list of zones and occupants
            self.zones = []
            self.occupants=[]

            if zones is not None:
                self.zones = zones
            if occupants is not None:
                self.occupants = occupants

        def __repr__(self):
            return '{}: {} {} {} {}'.format(self.__class__.__name__,
                self.id,
                self.name,
                self.zones,
                self.occupants
                )

        def __cmp__(self, other):
            if hasattr(other, 'getKey'):
                return self.getKey().__cmp__(other.getKey())

    # stochastic models
    class NoMASSModels(object):
        # model
        class Presence(object):
            # constructor I
            def __init__(self):
                self.enabled = False

        # model
        class Lights(object):
            # constructor I
            def __init__(self):
                self.enabled = False

        # model
        class AgentHeatGains(object):
            # constructor I
            def __init__(self):
                self.enabled = False

        # model
        class Heating(object):
            # constructor I
            def __init__(self):
                self.enabled = False

        # model and collection of items
        class Windows(object):
            class Window(object):
            	def getKey(self):
            		return self.id

            	def __init__(self, id=0, name='', aop=0, bopout=0, shapeop=0, a01arr=0, b01inarr=0, b01outarr=0, b01absprevarr=0, b01rnarr=0, a01int=0, b01inint=0, b01outint=0, b01presint=0, b01rnint=0, a01dep=0, b01outdep=0, b01absdep=0, b01gddep=0, a10dep=0, b10indep=0, b10outdep=0, b10absdep=0, b10gddep=0):
            		self.id = id
            		self.name = name
            		self.aop = aop
            		self.bopout = bopout
            		self.shapeop = shapeop
            		self.a01arr = a01arr
            		self.b01inarr = b01inarr
            		self.b01outarr = b01outarr
            		self.b01absprevarr = b01absprevarr
            		self.b01rnarr = b01rnarr
            		self.a01int = a01int
            		self.b01inint = b01inint
            		self.b01outint = b01outint
            		self.b01presint = b01presint
            		self.b01rnint = b01rnint
            		self.a01dep = a01dep
            		self.b01outdep = b01outdep
            		self.b01absdep = b01absdep
            		self.b01gddep = b01gddep
            		self.a10dep = a10dep
            		self.b10indep = b10indep
            		self.b10outdep = b10outdep
            		self.b10absdep = b10absdep
            		self.b10gddep = b10gddep

            	def __repr__(self):
            		return '{}: {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(self.__class__.__name__,
            			self.id,
            			self.name,
            			self.aop,
            			self.bopout,
            			self.shapeop,
            			self.a01arr,
            			self.b01inarr,
            			self.b01outarr,
            			self.b01absprevarr,
            			self.b01rnarr,
            			self.a01int,
            			self.b01inint,
            			self.b01outint,
            			self.b01presint,
            			self.b01rnint,
            			self.a01dep,
            			self.b01outdep,
            			self.b01absdep,
            			self.b01gddep,
            			self.a10dep,
            			self.b10indep,
            			self.b10outdep,
            			self.b10absdep,
            			self.b10gddep
            			)

            	def __cmp__(self, other):
            		if hasattr(other, 'getKey'):
            			return self.getKey().__cmp__(other.getKey())

            def clear(self):
                del self.windows[:]

            def append(self, objWindow):
                self.windows.append(objWindow)
                return

            # constructor I
            def __init__(self):
                self.enabled = False
                self.windows = []
                return
        # end of Windows

        # model and collection of items
        class Shades(object):
            class Shade(object):
            	def getKey(self):
            		return self.id

            	def __init__(self, id=0, name='', a01arr=0, b01inarr=0, b01sarr=0, a10arr=0, b10inarr=0, b10sarr=0, a01int=0, b01inint=0, b01sint=0, a10int=0, b10inint=0, b10sint=0, afullraise=0, boutfullraise=0, bsfullraise=0, bsfulllower=0, boutfulllower=0, afulllower=0, aSFlower=0, bSFlower=0, shapelower=0):
            		self.id = id
            		self.name = name
            		self.a01arr = a01arr
            		self.b01inarr = b01inarr
            		self.b01sarr = b01sarr
            		self.a10arr = a10arr
            		self.b10inarr = b10inarr
            		self.b10sarr = b10sarr
            		self.a01int = a01int
            		self.b01inint = b01inint
            		self.b01sint = b01sint
            		self.a10int = a10int
            		self.b10inint = b10inint
            		self.b10sint = b10sint
            		self.afullraise = afullraise
            		self.boutfullraise = boutfullraise
            		self.bsfullraise = bsfullraise
            		self.bsfulllower = bsfulllower
            		self.boutfulllower = boutfulllower
            		self.afulllower = afulllower
            		self.aSFlower = aSFlower
            		self.bSFlower = bSFlower
            		self.shapelower = shapelower

            	def __repr__(self):
            		return '{}: {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(self.__class__.__name__,
            			self.id,
            			self.name,
            			self.a01arr,
            			self.b01inarr,
            			self.b01sarr,
            			self.a10arr,
            			self.b10inarr,
            			self.b10sarr,
            			self.a01int,
            			self.b01inint,
            			self.b01sint,
            			self.a10int,
            			self.b10inint,
            			self.b10sint,
            			self.afullraise,
            			self.boutfullraise,
            			self.bsfullraise,
            			self.bsfulllower,
            			self.boutfulllower,
            			self.afulllower,
            			self.aSFlower,
            			self.bSFlower,
            			self.shapelower
            			)

            	def __cmp__(self, other):
            		if hasattr(other, 'getKey'):
            			return self.getKey().__cmp__(other.getKey())

            def clear(self):
                del self.shades[:]

            def append(self, objShade):
                self.shades.append(objShade)
                return

            # constructor I
            def __init__(self):
                self.enabled = False
                self.shades = []
                return
        # end of Shades

        # constructor
        def __init__(self):
            # set initial values
            self.presence = self.Presence()
            self.lights = self.Lights()
            self.agentHeatGains = self.AgentHeatGains()
            self.heating = self.Heating()
            self.windows = self.Windows()
            self.shades = self.Shades()

    # All classes are defined above this point

    def resetValues(self, insSimulation=None):
        if insSimulation is None:
            self.filename = ""
            self.sessionID = Utils.Constants.emptyGUID
            self.typeOfBuilding = str(Utils.Config.getValue("Default", "typeOfBuilding"))
            self.area = 11.41
            self.occupantDensity = Utils.Config.getDefaultOccupantDensity()
            self.numberOfOccupants = int(self.area // self.occupantDensity)
            self.seed = 0
            self.timeStepsPerHour = 12
            self.beginMonth = 1
            self.endMonth = 12
            self.beginDay = 1
            self.endDay = 31
            self.learn = False
            self.save = True
            self.eplusVersion = str(Utils.Config.getValue("Default", "eplusVersion"))
            self.numberOfReplicates = 0
            self.numberOfReplicatesRandom = 10

            self.idfFilename = Utils.Config.getDefaultIDF()
            self.weatherFilename = Utils.Config.getDefaultWeatherFile()
            self.outputDirectory = Utils.Config.getDefaultOutputDirectory()
            self.eplusLocation = Utils.Config.getEPlusLocation()

            self.randomWindow = True
            self.randomShade = True
            
            self.attachDayCtrl = True
            self.attachWinState0 = True

            self.building = self.Building()
            self.models = self.NoMASSModels()

            self.outputVariables = []
        else:
            self.filename = insSimulation.filename
            self.sessionID = insSimulation.sessionID
            self.typeOfBuilding = insSimulation.typeOfBuilding
            self.area = insSimulation.area
            self.occupantDensity = insSimulation.occupantDensity
            self.numberOfOccupants = insSimulation.numberOfOccupants
            self.seed = insSimulation.seed
            self.timeStepsPerHour = insSimulation.timeStepsPerHour
            self.beginMonth = insSimulation.beginMonth
            self.endMonth = insSimulation.endMonth
            self.beginDay = insSimulation.beginDay
            self.endDay = insSimulation.endDay
            self.learn = insSimulation.learn
            self.save = insSimulation.save
            self.eplusVersion = insSimulation.eplusVersion
            self.numberOfReplicates = insSimulation.numberOfReplicates
            self.numberOfReplicatesRandom = insSimulation.numberOfReplicatesRandom

            self.idfFilename = insSimulation.idfFilename
            self.weatherFilename = insSimulation.weatherFilename
            self.outputDirectory = insSimulation.outputDirectory
            self.eplusLocation = insSimulation.eplusLocation

            self.randomWindow = insSimulation.randomWindow
            self.randomShade = insSimulation.randomShade
            
            self.attachDayCtrl = insSimulation.attachDayCtrl
            self.attachWinState0 = insSimulation.attachWinState0

            self.building = self.Building()
            self.models = self.NoMASSModels()

            self.building.id = insSimulation.building.id
            self.building.name = insSimulation.building.name
            self.building.zones = insSimulation.building.zones
            self.building.occupants = insSimulation.building.occupants

            self.models.presence = insSimulation.models.presence
            self.models.windows = insSimulation.models.windows
            self.models.shades = insSimulation.models.shades
            self.models.lights = insSimulation.models.lights
            self.models.agentHeatGains = insSimulation.models.agentHeatGains
            self.models.heating = insSimulation.models.heating

            self.outputVariables = insSimulation.outputVariables
        return

    def loadFromFile(self, filename):
        self.__init__()
        self.filename = filename

        XMLtree = ElementTree.parse(self.filename)
        XMLroot = XMLtree.getroot()
        if XMLroot.tag.strip().lower() != "simulation":
            return False

        for child in XMLroot:
            if child.tag.strip().lower() == "typeofbuilding":
            	self.typeOfBuilding = str(child.text).strip()
            if child.tag.strip().lower() == "area":
            	self.area = float(child.text)
            if child.tag.strip().lower() == "numberofoccupants":
            	self.numberOfOccupants = int(child.text)
            if child.tag.strip().lower() == "seed":
            	self.seed = int(child.text)
            if child.tag.strip().lower() == "timestepsperhour":
            	self.timeStepsPerHour = int(child.text)
            if child.tag.strip().lower() == "beginmonth":
            	self.beginMonth = int(child.text)
            if child.tag.strip().lower() == "endmonth":
            	self.endMonth = int(child.text)
            if child.tag.strip().lower() == "beginday":
            	self.beginDay = int(child.text)
            if child.tag.strip().lower() == "endday":
            	self.endDay = int(child.text)
            if child.tag.strip().lower() == "learn":
            	self.learn = bool(child.text == "1")
            if child.tag.strip().lower() == "save":
            	self.save = bool(child.text == "1")
            if child.tag.strip().lower() == "eplusversion":
            	self.eplusVersion = str(child.text)

            if child.tag.strip().lower() == "numberofreplicates":
                self.numberOfReplicates = int(child.text)
            if child.tag.strip().lower() == "numberofreplicatesrandom":
                self.numberOfReplicatesRandom = int(child.text)


            if child.tag.strip().lower() == "idffile":
            	self.idfFilename = str(child.text)
            if child.tag.strip().lower() == "weatherfile":
            	self.weatherFilename = str(child.text)
            if child.tag.strip().lower() == "outputdirectory":
            	self.outputDirectory = str(child.text)
            if child.tag.strip().lower() == "epluslocation":
            	self.eplusLocation = str(child.text)

            if child.tag.strip().lower() == "randomwindow":
            	self.randomWindow = bool(child.text == "1")
            if child.tag.strip().lower() == "randomshade":
            	self.randomShade = bool(child.text == "1")
                
            if child.tag.strip().lower() == "attachdayctrl":
            	self.attachDayCtrl = bool(child.text == "1") or bool(child.text.lower() == "true")
            	#print("----------", child.text.lower(), "---------")
            if child.tag.strip().lower() == "attachwinstate0":
            	self.attachWinState0 = bool(child.text == "1") or bool(child.text.lower() == "true")
            
            if child.tag.strip().lower() == "buildings":
                for building in child.iter("building"):
                    self.building = self.Building()
                    self.building.id = building.attrib["id"]
                    self.building.name = building.attrib["name"]
                    for zone in building.iter("zone"):
                        newZone = self.Building.Zone()
                        for dataItem in zone:
                            if dataItem.tag.strip().lower() == "name":
                            	newZone.name = str(dataItem.text)
                            if dataItem.tag.strip().lower() == "activities":
                            	newZone.activities = str(dataItem.text)
                            if dataItem.tag.strip().lower() == "groundfloor":
                            	newZone.isGroundFloor = int(dataItem.text)
                            if dataItem.tag.strip().lower() == "windowcount":
                            	newZone.windowCount = int(dataItem.text)
                            if dataItem.tag.strip().lower() == "floorarea":
                            	newZone.floorArea = float(dataItem.text)
                        self.building.zones.append(newZone)
                        
            if child.tag.strip().lower() == "models":
                for model in child:
                    if model.tag.strip().lower() == "presence":
                        self.models.presence.enabled = bool(True if int(model.attrib["enabled"]) == 1 else False)
                    if model.tag.strip().lower() == "windows":
                        self.models.windows.enabled = bool(True if int(model.attrib["enabled"]) == 1 else False)
                    if model.tag.strip().lower() == "shades":
                        self.models.shades.enabled = bool(True if int(model.attrib["enabled"]) == 1 else False)
                    if model.tag.strip().lower() == "lights":
                        self.models.lights.enabled = bool(True if int(model.attrib["enabled"]) == 1 else False)
                    if model.tag.strip().lower() == "agentheatgains":
                        self.models.agentHeatGains.enabled = bool(True if int(model.attrib["enabled"]) == 1 else False)
                    if model.tag.strip().lower() == "heating":
                        self.models.heating.enabled = bool(True if int(model.attrib["enabled"]) == 1 else False)
                    
                    
            if child.tag.strip().lower() == "outputvariables":
                for variable in child.iter("eplusVariable"):
                    self.outputVariables.append(str(variable.text))
                    
                

    # end of loadFromFile

    def saveXML(self):
        output = {}
        output["error"] = False
        output["message"] = ""

        # try:
        XMLroot = ElementTree.Element('simulation')
        XMLchild = ElementTree.SubElement(XMLroot, 'simulationID')
        XMLchild.text = str(self.sessionID)
        XMLchild = ElementTree.SubElement(XMLroot, 'typeofbuilding')
        XMLchild.text = str(self.typeOfBuilding)
        XMLchild = ElementTree.SubElement(XMLroot, 'area')
        XMLchild.text = str(self.area)
        XMLchild = ElementTree.SubElement(XMLroot, 'numberOfOccupants')
        XMLchild.text = str(self.numberOfOccupants)
        XMLchild = ElementTree.SubElement(XMLroot, 'numberOfReplicates')
        XMLchild.text = str(self.numberOfReplicates)
        XMLchild = ElementTree.SubElement(XMLroot, 'numberOfReplicatesRandom')
        XMLchild.text = str(self.numberOfReplicatesRandom)
        XMLchild = ElementTree.SubElement(XMLroot, 'seed')
        XMLchild.text = '{0:g}'.format(self.seed)
        XMLchild = ElementTree.SubElement(XMLroot, 'timeStepsPerHour')
        XMLchild.text = str(self.timeStepsPerHour)
        XMLchild = ElementTree.SubElement(XMLroot, 'beginMonth')
        XMLchild.text = str(self.beginMonth)
        XMLchild = ElementTree.SubElement(XMLroot, 'endMonth')
        XMLchild.text = str(self.endMonth)
        XMLchild = ElementTree.SubElement(XMLroot, 'beginDay')
        XMLchild.text = str(self.beginDay)
        XMLchild = ElementTree.SubElement(XMLroot, 'endDay')
        XMLchild.text = str(self.endDay)
        XMLchild = ElementTree.SubElement(XMLroot, 'learn')
        XMLchild.text = str("1" if self.learn else "0")
        XMLchild = ElementTree.SubElement(XMLroot, 'save')
        XMLchild.text = str("1" if self.save else "0")
        XMLchild = ElementTree.SubElement(XMLroot, 'eplusVersion')
        XMLchild.text = str(self.eplusVersion)
        XMLchild = ElementTree.SubElement(XMLroot, 'idfFile')
        XMLchild.text = str(self.idfFilename)
        XMLchild = ElementTree.SubElement(XMLroot, 'weatherFile')
        XMLchild.text = str(self.weatherFilename)
        XMLchild = ElementTree.SubElement(XMLroot, 'outputDirectory')
        XMLchild.text = str(self.outputDirectory)
        XMLchild = ElementTree.SubElement(XMLroot, 'eplusLocation')
        XMLchild.text = str(self.eplusLocation)
        XMLchild = ElementTree.SubElement(XMLroot, 'randomWindow')
        XMLchild.text = str(self.randomWindow)
        XMLchild = ElementTree.SubElement(XMLroot, 'randomShade')
        XMLchild.text = str(self.randomShade)

        XMLchild = ElementTree.SubElement(XMLroot, 'attachDayCtrl')
        XMLchild.text = str(self.attachDayCtrl)
        XMLchild = ElementTree.SubElement(XMLroot, 'attachWinState0')
        XMLchild.text = str(self.attachWinState0)
        
        # buildings tag
        XMLBuildings = ElementTree.SubElement(XMLroot, 'buildings')
        XMLBuilding = ElementTree.SubElement(XMLBuildings, 'building')
        XMLBuilding.set("id", str(self.building.id))
        XMLBuilding.set("name", str(self.building.name))

        # append zones
        for zone in sorted(self.building.zones, key=lambda e: e.name):
            if zone.windowCount >= 0:
                XMLzone = ElementTree.SubElement(XMLBuilding, 'zone')
                XMLchild = ElementTree.SubElement(XMLzone, 'name')
                XMLchild.text = str(zone.name)
                XMLchild = ElementTree.SubElement(XMLzone, 'activities')
                XMLchild.text = str(zone.activities)
                XMLchild = ElementTree.SubElement(XMLzone, 'groundFloor')
                XMLchild.text = str("1" if zone.isGroundFloor else "0")
                XMLchild = ElementTree.SubElement(XMLzone, 'windowCount')
                XMLchild.text = str(zone.windowCount)
                XMLchild = ElementTree.SubElement(XMLzone, 'floorArea')
                XMLchild.text = str(zone.floorArea)
                # XMLchild = ElementTree.SubElement(XMLzone, 'varName')
                # XMLchild.text = str(zone.varName)

        # append agents
        XMLagents = ElementTree.SubElement(XMLBuilding, 'agents')
        i = 1
        for occupant in sorted(self.building.occupants, key=lambda e: e.id):
            # print(occupant, occupant.__dict__)
            XMLParent = ElementTree.SubElement(XMLagents, 'agent')
            XMLchild = ElementTree.SubElement(XMLParent, 'id')
            # XMLchild.text = str(occupant.id)
            XMLchild.text = str(i)
            XMLchild = ElementTree.SubElement(XMLParent, 'name')
            XMLchild.text = str(occupant.name)
            XMLchild = ElementTree.SubElement(XMLParent, 'description')
            XMLchild.text = str(occupant.description)
            XMLchild = ElementTree.SubElement(XMLParent, 'categoryID')
            XMLchild.text = str(occupant.categoryID)
            XMLchild = ElementTree.SubElement(XMLParent, 'category')
            XMLchild.text = str(occupant.category)
            XMLchild = ElementTree.SubElement(XMLParent, 'regionID')
            XMLchild.text = str(occupant.regionID)
            XMLchild = ElementTree.SubElement(XMLParent, 'region')
            XMLchild.text = str(occupant.region)
            XMLchild = ElementTree.SubElement(XMLParent, 'sectorID')
            XMLchild.text = str(occupant.sectorID)
            XMLchild = ElementTree.SubElement(XMLParent, 'sector')
            XMLchild.text = str(occupant.sector)

            zoneTag = "zone"
            if str(self.typeOfBuilding).strip().lower() == "office":
            	zoneTag = "office"
            elif str(self.typeOfBuilding).strip().lower() == "residential":
                zoneTag = "bedroom"

            XMLchild = ElementTree.SubElement(XMLParent, ('%sId' % (zoneTag)))
            XMLchild.text = str(occupant.zoneId)
            XMLchild = ElementTree.SubElement(XMLParent, zoneTag)
            XMLchild.text = str(occupant.zone)

            XMLchild = ElementTree.SubElement(XMLParent, 'power')
            XMLchild.text = str(occupant.power)
            XMLchild = ElementTree.SubElement(XMLParent, 'windowId')
            XMLchild.text = str(occupant.windowId)
            XMLchild = ElementTree.SubElement(XMLParent, 'window')
            XMLchild.text = str(occupant.window)
            XMLchild = ElementTree.SubElement(XMLParent, 'shadeId')
            XMLchild.text = str(occupant.shadeId)
            XMLchild = ElementTree.SubElement(XMLParent, 'shade')
            XMLchild.text = str(occupant.shade)
            # add the activity profile
            XMLprofile = ElementTree.SubElement(XMLParent, 'profile')
            XMLprofile.set("activityId", str(occupant.activityId))
            
            if str(self.typeOfBuilding).strip().lower() == "office":
                XMLchild = ElementTree.SubElement(XMLprofile, 'monday')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.monday)
                XMLchild = ElementTree.SubElement(XMLprofile, 'tuesday')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.tuesday)
                XMLchild = ElementTree.SubElement(XMLprofile, 'wednesday')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.wednesday)
                XMLchild = ElementTree.SubElement(XMLprofile, 'thursday')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.thursday)
                XMLchild = ElementTree.SubElement(XMLprofile, 'friday')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.friday)
                XMLchild = ElementTree.SubElement(XMLprofile, 'saturday')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.saturday)
                XMLchild = ElementTree.SubElement(XMLprofile, 'sunday')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.sunday)
            else:
                XMLchild = ElementTree.SubElement(XMLprofile, 'p0')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p0)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p1')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p1)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p2')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p2)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p3')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p3)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p4')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p4)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p5')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p5)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p6')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p6)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p7')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p7)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p8')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p8)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p9')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p9)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p10')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p10)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p11')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p11)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p12')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p12)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p13')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p13)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p14')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p14)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p15')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p15)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p16')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p16)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p17')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p17)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p18')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p18)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p19')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p19)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p20')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p20)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p21')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p21)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p22')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p22)
                XMLchild = ElementTree.SubElement(XMLprofile, 'p23')
                XMLchild.text = ','.join(str(x) for x in occupant.profile.p23)

            XMLchild = ElementTree.SubElement(XMLParent, 'sex')
            XMLchild.text = str(occupant.sex)
            XMLchild = ElementTree.SubElement(XMLParent, 'famStateGroup')
            XMLchild.text = str(occupant.familyID)
            XMLchild = ElementTree.SubElement(XMLParent, 'edtry')
            XMLchild.text = str(occupant.educationID)
            XMLchild = ElementTree.SubElement(XMLParent, 'ageGroup')
            XMLchild.text = str(occupant.ageGroup)
            XMLchild = ElementTree.SubElement(XMLParent, 'ownComputer')
            XMLchild.text = str(1 if occupant.ownComputer else 0)
            XMLchild = ElementTree.SubElement(XMLParent, 'isRetired')
            XMLchild.text = str(1 if occupant.isRetired else 0)
            XMLchild = ElementTree.SubElement(XMLParent, 'civStateGroup')
            XMLchild.text = str(1 if occupant.isMarried else 0)
            XMLchild = ElementTree.SubElement(XMLParent, 'isUnEmployed')
            XMLchild.text = str(1 if occupant.isUnEmployed else 0)
            i += 1

        # append NoMASS models
        XMLModels = ElementTree.SubElement(XMLroot, 'models')

        # aggregate presence
        XMLModel = ElementTree.SubElement(XMLModels, 'presence')
        XMLModel.set("enabled", str("1" if self.models.presence.enabled else "0"))

        # aggregate Windows
        XMLModel = ElementTree.SubElement(XMLModels, 'windows')
        XMLModel.set("enabled", str("1" if self.models.windows.enabled else "0"))

        # aggregate Window elements
        #print("type(self.models.windows.windows)", type(self.models.windows.windows))
        ##print(self.models.windows.windows.sort(key=lambda x: x[0]['ID'], reverse=False))
        #print(sorted(self.models.windows.windows, key=lambda e: e.name))
        #print("type(sorted(self.models.windows.windows))", type(sorted(self.models.windows.windows)))
        #print("sorted(self.models.windows.windows)", sorted(self.models.windows.windows))
        #for window in sorted(self.models.windows.windows):
        for window in sorted(self.models.windows.windows, key=lambda e: e.name): # updated on 25.10.2021 daps
            XMLParent = ElementTree.SubElement(XMLModel, 'window')
            XMLchild = ElementTree.SubElement(XMLParent, 'id')
            XMLchild.text = str(window.id)
            XMLchild = ElementTree.SubElement(XMLParent, 'name')
            XMLchild.text = str(window.name)
            XMLchild = ElementTree.SubElement(XMLParent, 'aop')
            XMLchild.text = str(window.aop)
            XMLchild = ElementTree.SubElement(XMLParent, 'bopout')
            XMLchild.text = str(window.bopout)
            XMLchild = ElementTree.SubElement(XMLParent, 'shapeop')
            XMLchild.text = str(window.shapeop)
            XMLchild = ElementTree.SubElement(XMLParent, 'a01arr')
            XMLchild.text = str(window.a01arr)
            XMLchild = ElementTree.SubElement(XMLParent, 'b01inarr')
            XMLchild.text = str(window.b01inarr)
            XMLchild = ElementTree.SubElement(XMLParent, 'b01outarr')
            XMLchild.text = str(window.b01outarr)
            XMLchild = ElementTree.SubElement(XMLParent, 'b01absprevarr')
            XMLchild.text = str(window.b01absprevarr)
            XMLchild = ElementTree.SubElement(XMLParent, 'b01rnarr')
            XMLchild.text = str(window.b01rnarr)
            XMLchild = ElementTree.SubElement(XMLParent, 'a01int')
            XMLchild.text = str(window.a01int)
            XMLchild = ElementTree.SubElement(XMLParent, 'b01inint')
            XMLchild.text = str(window.b01inint)
            XMLchild = ElementTree.SubElement(XMLParent, 'b01outint')
            XMLchild.text = str(window.b01outint)
            XMLchild = ElementTree.SubElement(XMLParent, 'b01presint')
            XMLchild.text = str(window.b01presint)
            XMLchild = ElementTree.SubElement(XMLParent, 'b01rnint')
            XMLchild.text = str(window.b01rnint)
            XMLchild = ElementTree.SubElement(XMLParent, 'a01dep')
            XMLchild.text = str(window.a01dep)
            XMLchild = ElementTree.SubElement(XMLParent, 'b01outdep')
            XMLchild.text = str(window.b01outdep)
            XMLchild = ElementTree.SubElement(XMLParent, 'b01absdep')
            XMLchild.text = str(window.b01absdep)
            XMLchild = ElementTree.SubElement(XMLParent, 'b01gddep')
            XMLchild.text = str(window.b01gddep)
            XMLchild = ElementTree.SubElement(XMLParent, 'a10dep')
            XMLchild.text = str(window.a10dep)
            XMLchild = ElementTree.SubElement(XMLParent, 'b10indep')
            XMLchild.text = str(window.b10indep)
            XMLchild = ElementTree.SubElement(XMLParent, 'b10outdep')
            XMLchild.text = str(window.b10outdep)
            XMLchild = ElementTree.SubElement(XMLParent, 'b10absdep')
            XMLchild.text = str(window.b10absdep)
            XMLchild = ElementTree.SubElement(XMLParent, 'b10gddep')
            XMLchild.text = str(window.b10gddep)

        # aggregate Shades
        XMLModel = ElementTree.SubElement(XMLModels, 'shades')
        XMLModel.set("enabled", str("1" if self.models.shades.enabled else "0"))                

        # aggregate Shade elements
        #for shade in sorted(self.models.shades.shades):
        for shade in sorted(self.models.shades.shades, key=lambda e: e.name):  # updated on 25.10.2021 daps
            XMLParent = ElementTree.SubElement(XMLModel, 'shade')
            XMLchild = ElementTree.SubElement(XMLParent, 'id')
            XMLchild.text = str(shade.id)
            XMLchild = ElementTree.SubElement(XMLParent, 'name')
            XMLchild.text = str(shade.name)
            XMLchild = ElementTree.SubElement(XMLParent, 'a01arr')
            XMLchild.text = str(shade.a01arr)
            XMLchild = ElementTree.SubElement(XMLParent, 'b01inarr')
            XMLchild.text = str(shade.b01inarr)
            XMLchild = ElementTree.SubElement(XMLParent, 'b01sarr')
            XMLchild.text = str(shade.b01sarr)
            XMLchild = ElementTree.SubElement(XMLParent, 'a10arr')
            XMLchild.text = str(shade.a10arr)
            XMLchild = ElementTree.SubElement(XMLParent, 'b10inarr')
            XMLchild.text = str(shade.b10inarr)
            XMLchild = ElementTree.SubElement(XMLParent, 'b10sarr')
            XMLchild.text = str(shade.b10sarr)
            XMLchild = ElementTree.SubElement(XMLParent, 'a01int')
            XMLchild.text = str(shade.a01int)
            XMLchild = ElementTree.SubElement(XMLParent, 'b01inint')
            XMLchild.text = str(shade.b01inint)
            XMLchild = ElementTree.SubElement(XMLParent, 'b01sint')
            XMLchild.text = str(shade.b01sint)
            XMLchild = ElementTree.SubElement(XMLParent, 'a10int')
            XMLchild.text = str(shade.a10int)
            XMLchild = ElementTree.SubElement(XMLParent, 'b10inint')
            XMLchild.text = str(shade.b10inint)
            XMLchild = ElementTree.SubElement(XMLParent, 'b10sint')
            XMLchild.text = str(shade.b10sint)
            XMLchild = ElementTree.SubElement(XMLParent, 'afullraise')
            XMLchild.text = str(shade.afullraise)
            XMLchild = ElementTree.SubElement(XMLParent, 'boutfullraise')
            XMLchild.text = str(shade.boutfullraise)
            XMLchild = ElementTree.SubElement(XMLParent, 'bsfullraise')
            XMLchild.text = str(shade.bsfullraise)
            XMLchild = ElementTree.SubElement(XMLParent, 'bsfulllower')
            XMLchild.text = str(shade.bsfulllower)
            XMLchild = ElementTree.SubElement(XMLParent, 'boutfulllower')
            XMLchild.text = str(shade.boutfulllower)
            XMLchild = ElementTree.SubElement(XMLParent, 'afulllower')
            XMLchild.text = str(shade.afulllower)
            XMLchild = ElementTree.SubElement(XMLParent, 'aSFlower')
            XMLchild.text = str(shade.aSFlower)
            XMLchild = ElementTree.SubElement(XMLParent, 'bSFlower')
            XMLchild.text = str(shade.bSFlower)
            XMLchild = ElementTree.SubElement(XMLParent, 'shapelower')
            XMLchild.text = str(shade.shapelower)

        # aggregate Lights
        XMLModel = ElementTree.SubElement(XMLModels, 'lights')
        XMLModel.set("enabled", str("1" if self.models.lights.enabled else "0"))

        # aggregate HeatGains
        XMLModel = ElementTree.SubElement(XMLModels, 'agentHeatGains')
        XMLModel.set("enabled", str("1" if self.models.agentHeatGains.enabled else "0"))

        # aggregate Heating
        XMLModel = ElementTree.SubElement(XMLModels, 'heating')
        XMLModel.set("enabled", str("1" if self.models.heating.enabled else "0"))

        # selected output variables
        XMLOutputVariables = ElementTree.SubElement(XMLroot, 'outputVariables')
        for i in range(len(self.outputVariables)):
            XMLchild = ElementTree.SubElement(XMLOutputVariables, 'eplusVariable')
            XMLchild.text = self.outputVariables[i]

        Utils.XML.setIndentation(XMLroot)
        XMLtree = ElementTree.ElementTree(XMLroot)
        XMLtree.write(self.filename,"UTF-8")

        return output
    # end of saveXML(self):

    # constructor I
    def __init__(self, insSimulation=None):
        self.filename = ""
        self.sessionID = Utils.Constants.emptyGUID
        self.typeOfBuilding = ""
        self.area = 0
        self.occupantDensity = 0
        self.numberOfOccupants = 0
        self.seed = 0
        self.timeStepsPerHour = 0
        self.beginMonth = 1
        self.endMonth = 12
        self.beginDay = 1
        self.endDay = 31
        self.learn = False
        self.save = True
        self.eplusVersion = "Undefined"
        self.numberOfReplicates = 0
        self.numberOfReplicatesRandom = 1

        self.idfFilename = ""
        self.weatherFilename = ""
        self.outputDirectory = ""
        self.eplusLocation = ""

        self.outputVariables = []

        self.randomWindow = True
        self.randomShade = True

        self.building = self.Building()
        self.models = self.NoMASSModels()

        self.resetValues(insSimulation)
        return
# end of class Simulation
