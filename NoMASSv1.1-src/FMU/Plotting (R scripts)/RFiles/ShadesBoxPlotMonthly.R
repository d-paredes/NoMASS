
suppressPackageStartupMessages(library(plyr))
suppressPackageStartupMessages(library(data.table))

# Change working directory

locationToProcess = "/Volumes/Disk2/results/BaseCaseGENOfficeAll"
locationToProcessPDF = "~/Dropbox/Apps/Texpad/sensistivityanalysis/Images/OfficeGENShadeState.pdf"

locationToProcess = "/Volumes/Disk2/results/BaseCaseUKOfficeAll"
locationToProcessPDF = "~/Dropbox/Apps/Texpad/sensistivityanalysis/Images/OfficeUKShadeState.pdf"


dateT = function(x) {
  return((as.integer(strftime(strptime(x,"%m/%d %H:%M:%S"), format="%m"))))
}

setwd(locationToProcess)

timeStep = list.files(pattern="timestep.*[.]csv")
monthlyShadeState <- data.frame()

for (i in 1:length(timeStep)) {
  x = fread(timeStep[[i]], sep=",", header=TRUE)
  x$month = unlist(lapply(x$`Date/Time`,dateT))
  monthlyShadeState = rbind(monthlyShadeState, 
    ddply(x, .(month), summarize, 
          sum=mean(`BLOCK1:ZONE1_WALL_5_0_0_0_0_0_WIN:Window Shading Fraction [Fraction](TimeStep)`)))
}

pdf(locationToProcessPDF)

boxplot(sum ~ month, data=monthlyShadeState, main="",
  xlab="Month", ylab="Mean Unshaded Fraction", outline=FALSE, ylim=c(0,1))

dev.off()
