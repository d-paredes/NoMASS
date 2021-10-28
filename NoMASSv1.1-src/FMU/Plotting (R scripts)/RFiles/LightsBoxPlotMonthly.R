
suppressPackageStartupMessages(library(plyr))
suppressPackageStartupMessages(library(data.table))

# Change working directory

locationToProcess = "/Volumes/Disk2/results/BaseCaseGENOfficeAll"
locationToProcessPDF = "~/Dropbox/Apps/Texpad/sensistivityanalysis/Images/OfficeGENLightState.pdf"

locationToProcess = "/Volumes/Disk2/results/BaseCaseUKOfficeAll"
locationToProcessPDF = "~/Dropbox/Apps/Texpad/sensistivityanalysis/Images/OfficeUKLightState.pdf"


dateT = function(x) {
  return((as.integer(strftime(strptime(x,"%m/%d %H:%M:%S"), format="%m"))))
}

setwd(locationToProcess)

timeStep = list.files(pattern="timestep.*[.]csv")
monthlyLightState <- data.frame()
i=1
for (i in 1:length(timeStep)) {
  x = fread(timeStep[[i]], sep=",", header=TRUE)
  x$month = unlist(lapply(x$`Date/Time`,dateT))
  monthlyLightState = rbind(monthlyLightState, 
    ddply(x, .(month), summarize, 
          sum=mean(`BLOCK1:ZONE1LIGHTSTATE:Schedule Value [](TimeStep)`)))
}

pdf(locationToProcessPDF)

boxplot(sum ~ month, data=monthlyLightState, main = "",
  xlab="Month", ylab="Proportion Of Time Ligths Are On", outline=FALSE, ylim=c(0,0.4)
)

dev.off()
