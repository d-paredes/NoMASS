
suppressPackageStartupMessages(library(plyr))

suppressPackageStartupMessages(library(data.table))

# Change working directory



locationToProcess = "/Volumes/Disk2/results/Cum/BaseCaseGENHouseAll"

locationToProcess = "/media/jake/4TB/results/HouseLearn/Learned"

setwd(locationToProcess)

convertJulesToWMS <- function(value, size)
  (value)

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
    monthly[[i]]$BLOCK1.KITCHEN.Zone.Mean.Air.Temperature..C..Monthly., 
    convertJulesToWMS,  size = 10)
  
  LIVINGROOMD[i,] = lapply(
    monthly[[i]]$BLOCK1.LIVINGROOM.Zone.Mean.Air.Temperature..C..Monthly., 
    convertJulesToWMS,  size = 11.57)
  
  BEDROOMD[i,] = lapply(
    monthly[[i]]$BLOCK2.BEDROOM.Zone.Mean.Air.Temperature..C..Monthly., 
    convertJulesToWMS,  size = 6.59)
  
  BATHROOMD[i,] = lapply(
    monthly[[i]]$BLOCK2.BATHROOM.Zone.Mean.Air.Temperature..C..Monthly., 
    convertJulesToWMS,  size = 1.78)
  
  MASTERBEDROOMD[i,] = lapply(
    monthly[[i]]$BLOCK2.MASTERBEDROOM.Zone.Mean.Air.Temperature..C..Monthly., 
    convertJulesToWMS,  size = 9.06)
  
  OFFICED[i,] = lapply(
    monthly[[i]]$BLOCK2.OFFICE.Zone.Mean.Air.Temperature..C..Monthly., 
    convertJulesToWMS,  size = 2.24)
  
}

locationToProcessPDF = "/home/jake/Dropbox/Apps/Texpad/Includes/Images/boxplotMonthlyAirtempHouse.pdf"
pdf(locationToProcessPDF)
par(mfrow=c(2,3))
par(mar=c(1,2,1,0)+0.1,mgp=c(1,0,0))

boxplot(
  KITCHEND, main = "",
  xlab = "", ylab = "Mean Monthly Air Temperature",outline = FALSE, ylim = c(15,30),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=FALSE)
Axis(side=2, tck = 0.03)
title("Kitchen", line = -1)
boxplot(
  LIVINGROOMD, main = "",
  xlab = "", ylab = "",outline = FALSE, ylim = c(15,30),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=FALSE)
Axis(side=2, tck = 0.03)
title("Living Room", line = -1)
boxplot(
  MASTERBEDROOMD, main = "",
  xlab = "", ylab = "",outline = FALSE, ylim = c(15,30),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=FALSE)
Axis(side=2, tck = 0.03)
title("Master Bedroom", line = -1)
boxplot(
  BEDROOMD, main = "",
  xlab = "", ylab = "",outline = FALSE, ylim = c(15,30),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=FALSE)
Axis(side=2, tck = 0.03)
title("Bedroom", line = -1)

boxplot(
  BATHROOMD, main = "",
  xlab = "", ylab = "",outline = FALSE, ylim = c(15,30),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=FALSE)
Axis(side=2, tck = 0.03)
title("Bathroom", line = -1)

boxplot(
  OFFICED, main = "",
  xlab = "", ylab = "",outline = FALSE, ylim = c(15,30),
  axes=FALSE, frame.plot=TRUE
)
Axis(side=1, labels=FALSE)
Axis(side=2, tck = 0.03)
title("Office", line = -1)



dev.off()

