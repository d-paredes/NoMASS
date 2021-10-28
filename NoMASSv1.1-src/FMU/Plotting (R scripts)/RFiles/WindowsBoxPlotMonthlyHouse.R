
suppressPackageStartupMessages(library(plyr))
suppressPackageStartupMessages(library(data.table))

# Change working directory


locationToProcess = "/Volumes/Disk2/results/BaseCaseGENHouseDeterministic"

locationToProcess = "/Volumes/Disk2/results/HouseLearnWindowH/Stochastic"
locationToProcessPDF = "~/Dropbox/Apps/Texpad/Includes/Images/HouseGENWindowStateStochastic.pdf"
locationToProcess = "/Volumes/Disk2/results/HouseLearnWindowH/Learned"
locationToProcess = "/Volumes/Disk2/results/Learned"
locationToProcessPDF = "~/Dropbox/Apps/Texpad/Includes/Images/HouseGENWindowStateLearned.pdf"


locationToProcess = "/Volumes/Disk2/results/Cum/BaseCaseGENHouseAll"
locationToProcess = "/Volumes/2tb/PhD/results-16-04-13/results/Cum/BaseCaseGENHouseAll"
locationToProcess = "/Users/jake/Desktop/BaseCaseGENHouseAll"
locationToProcessPDF = "~/Desktop/Images/HouseGENWindowState.pdf"
locationToProcessPDF2 = "~/Desktop/Images/HouseGENWindowState2.pdf"



dateT = function(x) {
  return((as.integer(strftime(strptime(x,"%m/%d %H:%M:%S"), format="%m"))))
}

setwd(locationToProcess)

timeStep = list.files(pattern="timestep.*[.]csv.*")
len =length(timeStep)
len = 100
KITCHEN <- data.frame()
LIVINGROOM <- data.frame()
BEDROOM <- data.frame()
BATHROOM <- data.frame()
MASTERBEDROOM <- data.frame()
OFFICE <- data.frame()
i = 1
for (i in 1:len) {
  print(i)
  x = read.csv(timeStep[[i]], sep=",", header=TRUE)
  x$month = unlist(lapply(x$Date.Time,dateT))
  KITCHEN = rbind(KITCHEN, 
      ddply(x, .(month), summarize,
      sum=mean(BLOCK1.KITCHEN_WALL_2_0_0_0_0_0_WIN.AFN.Surface.Venting.Window.or.Door.Opening.Factor....TimeStep.)))
  LIVINGROOM = rbind(LIVINGROOM, 
      ddply(x, .(month), summarize,
      sum=mean(BLOCK1.LIVINGROOM_WALL_2_0_0_0_0_0_WIN.AFN.Surface.Venting.Window.or.Door.Opening.Factor....TimeStep.)))
  BEDROOM = rbind(BEDROOM, 
      ddply(x, .(month), summarize,
      sum=mean(BLOCK2.BEDROOM_WALL_4_0_0_0_0_0_WIN.AFN.Surface.Venting.Window.or.Door.Opening.Factor....TimeStep.)))
  BATHROOM = rbind(BATHROOM, 
      ddply(x, .(month), summarize,
      sum=mean(BLOCK2.BATHROOM_WALL_2_0_0_0_0_0_WIN.AFN.Surface.Venting.Window.or.Door.Opening.Factor....TimeStep.)))
  MASTERBEDROOM = rbind(MASTERBEDROOM, 
      ddply(x, .(month), summarize,
      sum=mean(BLOCK2.MASTERBEDROOM_WALL_7_0_0_0_0_0_WIN.AFN.Surface.Venting.Window.or.Door.Opening.Factor....TimeStep.)))
  OFFICE = rbind(OFFICE, 
      ddply(x, .(month), summarize,
      sum=mean(BLOCK2.OFFICE_WALL_2_0_0_0_0_0_WIN.AFN.Surface.Venting.Window.or.Door.Opening.Factor....TimeStep.)))
}

pdf(locationToProcessPDF)

par(mar=c(1,2,2,0)+0.3,mgp=c(1,0,0))
par(mfrow=c(2,5))
boxplot(
  sum ~ month,data = KITCHEN, main = "Kitchen", 
  xlab="Month", ylab="", outline=FALSE, ylim=c(0,0.2),
  axes=FALSE, frame.plot=TRUE
)
mtext("Proportion Of Time Open", side=2, line=1, cex=1)
Axis(side=1, labels=TRUE, mgp=c(0, .6, 0), las=2)
Axis(side=2, tck = 0.03)
boxplot(
  sum ~ month,data = LIVINGROOM, main = "Livingroom", 
  xlab="Month", ylab="", outline=FALSE, ylim=c(0,0.2),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=TRUE, mgp=c(0, .6, 0), las=2)
Axis(side=2, tck = 0.03)

boxplot(
  sum ~ month,data = MASTERBEDROOM, main = "Masterbedroom", 
  xlab="Month", ylab="", outline=FALSE, ylim=c(0,0.2),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=TRUE, mgp=c(0, .6, 0), las=2)
Axis(side=2, tck = 0.03)
boxplot(
  sum ~ month,data = BEDROOM, main = "Bedroom", 
  xlab="Month", ylab="", outline=FALSE, ylim=c(0,0.2),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=TRUE, mgp=c(0, .6, 0), las=2)
Axis(side=2, tck = 0.03)

boxplot(
  sum ~ month,data = BATHROOM, main = "Bathroom", 
  xlab="Month", ylab="", outline=FALSE, ylim=c(0,0.2),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=TRUE, mgp=c(0, .6, 0), las=2)
Axis(side=2, tck = 0.03)

dev.off()
#pdf(locationToProcessPDF2)

par(mar=c(1,2,2,0)+0.3,mgp=c(1,0,0))
par(mfrow=c(2,4))
boxplot(
  sum ~ month,data = KITCHEN, main = "", 
  xlab="q", ylab="", outline=FALSE, ylim=c(0,0.2),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=TRUE, mgp=c(0, .6, 0), las=2)
Axis(side=2, tck = 0.03)
mtext("Proportion Of Time Open", side=2, line=1, cex=1)
title("Kitchen", line = 1)
boxplot(
  sum ~ month,data = LIVINGROOM, main = "", 
  xlab="", ylab="", outline=FALSE, ylim=c(0,0.2),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=TRUE, mgp=c(0, .6, 0), las=2)
Axis(side=2, tck = 0.03)
title("Living Room", line = 1)
boxplot(
  sum ~ month,data = MASTERBEDROOM, main = "", 
  xlab="", ylab="", outline=FALSE, ylim=c(0,0.2),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=TRUE, mgp=c(0, .6, 0), las=2)
Axis(side=2, tck = 0.03)
title("Master Bedroom", line = 1)
boxplot(
  sum ~ month,data = BATHROOM, main = "", 
  xlab="", ylab="", outline=FALSE, ylim=c(0,0.2),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=TRUE, mgp=c(0, .6, 0), las=2)
Axis(side=2, tck = 0.03)
title("Bathroom", line = 1)


dev.off()




locationToProcessPDF = "~/Dropbox/Apps/Texpad/Includes/Images/HouseGENWindowStateLearned.pdf"



pdf(locationToProcessPDF)
par(mfrow=c(2,5))

par(mar=c(1,2,2,1)+0.1,mgp=c(1,0,0))
boxplot(
  sum ~ month,data = KITCHEN, main = "", 
  xlab="q", ylab="Proportion Of Time Open", outline=FALSE, ylim=c(0,1.1),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=FALSE)
Axis(side=2, tck = 0.03)
title("Kitchen", line = -1)
boxplot(
  sum ~ month,data = LIVINGROOM, main = "", 
  xlab="", ylab="", outline=FALSE, ylim=c(0,1.1),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=FALSE)
Axis(side=2, tck = 0.03)
title("Living Room", line = -1)
boxplot(
  sum ~ month,data = MASTERBEDROOM, main = "", 
  xlab="", ylab="", outline=FALSE, ylim=c(0,1.1),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=FALSE)
Axis(side=2, tck = 0.03)
title("Master Bedroom", line = -1)
boxplot(
  sum ~ month,data = BEDROOM, main = "", 
  xlab="", ylab="", outline=FALSE, ylim=c(0,1.1),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=FALSE)
Axis(side=2, tck = 0.03)
title("Bedroom", line = -1)
boxplot(
  sum ~ month,data = BATHROOM, main = "", 
  xlab="", ylab="", outline=FALSE, ylim=c(0,1.1),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=FALSE)
Axis(side=2, tck = 0.03)
title("Bathroom", line = -1)
dev.off()



boxplot(
  KITCHEND, main = "",
  xlab = "", ylab = "Heating Demand(kWh/m2.y)",outline = FALSE, ylim = c(0,25),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=FALSE)
Axis(side=2, tck = 0.03)
title("Kitchen", line = -1)
boxplot(
  LIVINGROOMD, main = "",
  xlab = "", ylab = "",outline = FALSE, ylim = c(0,25),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=FALSE)
Axis(side=2, tck = 0.03)
title("Living Room", line = -1)
boxplot(
  MASTERBEDROOMD, main = "",
  xlab = "", ylab = "",outline = FALSE, ylim = c(0,25),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=FALSE)
Axis(side=2, tck = 0.03)
title("Master Bedroom", line = -1)
boxplot(
  BEDROOMD, main = "",
  xlab = "", ylab = "",outline = FALSE, ylim = c(0,25),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=FALSE)
Axis(side=2, tck = 0.03)
title("Bedroom", line = -1)

boxplot(
  BATHROOMD, main = "",
  xlab = "", ylab = "",outline = FALSE, ylim = c(0,25),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=FALSE)
Axis(side=2, tck = 0.03)
title("Bathroom", line = -1)


dev.off()

locationToProcessPDF = "~/Dropbox/Apps/Texpad/sensistivityanalysis/Images/HouseGENWindowStateOff.pdf"

pdf(locationToProcessPDF)
par(mfrow=c(2,1))

par(mar=c(3,5,1,1)+0.1)

boxplot(
  sum ~ month,data = OFFICE, main = "", 
  xlab="", ylab="Window Mean State", outline=FALSE, ylim=c(0,0.7),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1,las=2, at = c(1:12),labels=c("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"))
Axis(side=2,las=2)

boxplot(
  OFFICED, main = "",las=2,
  xlab = "", ylab = "Heating Demand\n(kWh/m2.y)",outline = FALSE, ylim = c(0,4)
)

dev.off()





