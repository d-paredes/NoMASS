
suppressPackageStartupMessages(library(plyr))

suppressPackageStartupMessages(library(data.table))

# Change working directory



locationToProcess = "/Volumes/Disk2/results/Cum/BaseCaseGENHouseAll"

locationToProcess = "/media/jake/4TB/results/HouseLearn/Learned"
locationToProcess = "/Users/jake/Desktop/BaseCaseGENHouseAll"
setwd(locationToProcess)

convertJulesToWMS <- function(value, size)
  (value * 0.0000002778) / size

officeSize = 67.17

monthly <- list.files(pattern = "monthly.*[.]csv")
monthly <- lapply(monthly, read.csv)
len = length(monthly)
len = 100

KITCHEND <-
  data.frame(
    "Jan" = NA,"Feb" = NA,"Mar" = NA,"Apr" = NA,"May" = NA,"Jun" = NA,"Jul" =
      NA,"Aug" = NA,"Sep" = NA,"Oct" = NA,"Nov" = NA,"Dec" = NA
  )

LIVINGROOMD <-
  data.frame(
    "Jan" = NA,"Feb" = NA,"Mar" = NA,"Apr" = NA,"May" = NA,"Jun" = NA,"Jul" =
      NA,"Aug" = NA,"Sep" = NA,"Oct" = NA,"Nov" = NA,"Dec" = NA
  )
BEDROOMD <-
  data.frame(
    "Jan" = NA,"Feb" = NA,"Mar" = NA,"Apr" = NA,"May" = NA,"Jun" = NA,"Jul" =
      NA,"Aug" = NA,"Sep" = NA,"Oct" = NA,"Nov" = NA,"Dec" = NA
  )
BATHROOMD <-
  data.frame(
    "Jan" = NA,"Feb" = NA,"Mar" = NA,"Apr" = NA,"May" = NA,"Jun" = NA,"Jul" =
      NA,"Aug" = NA,"Sep" = NA,"Oct" = NA,"Nov" = NA,"Dec" = NA
  )
MASTERBEDROOMD <-
  data.frame(
    "Jan" = NA,"Feb" = NA,"Mar" = NA,"Apr" = NA,"May" = NA,"Jun" = NA,"Jul" =
      NA,"Aug" = NA,"Sep" = NA,"Oct" = NA,"Nov" = NA,"Dec" = NA
  )
OFFICED <-
  data.frame(
    "Jan" = NA,"Feb" = NA,"Mar" = NA,"Apr" = NA,"May" = NA,"Jun" = NA,"Jul" =
      NA,"Aug" = NA,"Sep" = NA,"Oct" = NA,"Nov" = NA,"Dec" = NA
  )


for (i in 1:len) {
  KITCHEND[i,] = lapply(
    monthly[[i]]$BLOCK1.KITCHEN.Zone.Air.System.Sensible.Heating.Energy..J..Monthly., 
    convertJulesToWMS,  size = 10)
  LIVINGROOMD[i,] = lapply(
    monthly[[i]]$BLOCK1.LIVINGROOM.Zone.Air.System.Sensible.Heating.Energy..J..Monthly., 
    convertJulesToWMS,  size = 11.57)
  
  BEDROOMD[i,] = lapply(
    monthly[[i]]$BLOCK2.BEDROOM.Zone.Air.System.Sensible.Heating.Energy..J..Monthly., 
    convertJulesToWMS,  size = 6.59)
  
  BATHROOMD[i,] = lapply(
    monthly[[i]]$BLOCK2.BATHROOM.Zone.Air.System.Sensible.Heating.Energy..J..Monthly., 
    convertJulesToWMS,  size = 1.78)
  
  MASTERBEDROOMD[i,] = lapply(
    monthly[[i]]$BLOCK2.MASTERBEDROOM.Zone.Air.System.Sensible.Heating.Energy..J..Monthly., 
    convertJulesToWMS,  size = 9.06)
  
  OFFICED[i,] = lapply(
    monthly[[i]]$BLOCK2.OFFICE.Zone.Air.System.Sensible.Heating.Energy..J..Monthly., 
    convertJulesToWMS,  size = 2.24)
  
}


locationToProcessPDF2 = "~/Desktop/Images/HouseGENWindowState2.pdf"
pdf(locationToProcessPDF2)

par(mar=c(5,5,1,2)+0.1)


par(mar=c(1,2,2,0)+0.3,mgp=c(1,0,0))
par(mfrow=c(2,5))
boxplot(
  KITCHEND, main = "",
  xlab = "", ylab = "",outline = FALSE, ylim = c(0,25),
  axes=FALSE, frame.plot=TRUE
)
mtext("Heating Demand(kWh/m2.y)", side=2, line=1, cex=1)

Axis(side=1, labels=TRUE, mgp=c(0, .6, 0), las=2)
Axis(side=2, tck = 0.03)

boxplot(
  LIVINGROOMD, main = "",
  xlab = "", ylab = "",outline = FALSE, ylim = c(0,25),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=TRUE, mgp=c(0, .6, 0), las=2)
Axis(side=2, tck = 0.03)


boxplot(
  MASTERBEDROOMD, main = "",
  xlab = "", ylab = "",outline = FALSE, ylim = c(0,25),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=TRUE, mgp=c(0, .6, 0), las=2)
Axis(side=2, tck = 0.03)


boxplot(
  BEDROOMD, main = "",
  xlab = "", ylab = "",outline = FALSE, ylim = c(0,25),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=TRUE, mgp=c(0, .6, 0), las=2)
Axis(side=2, tck = 0.03)
boxplot(
  BATHROOMD, main = "",
  xlab = "", ylab = "",outline = FALSE, ylim = c(0,25),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=TRUE, mgp=c(0, .6, 0), las=2)
Axis(side=2, tck = 0.03)
#boxplot(
#  OFFICED, main = "",
#  xlab = "", ylab = "",outline = FALSE, ylim = c(0,25)
#)

dev.off()
