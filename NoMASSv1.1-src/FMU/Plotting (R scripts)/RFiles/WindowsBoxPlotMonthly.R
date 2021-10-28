
suppressPackageStartupMessages(library(plyr))
library("parallel", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")

# Change working directory

locationToProcess = '/Volumes/Disk2/results/OfficeSocial/Social1'

locationToProcess = '/Volumes/Disk2/results/socialLinux'
locationToProcess = '/Volumes/Disk2/results/socialLinux1'


locationToProcess = "/Volumes/Disk2/results/BaseCaseGENOfficeAll"
locationToProcessPDF = "~/Dropbox/Apps/Texpad/sensistivityanalysis/Images/OfficeGENWindowState.pdf"

locationToProcess = "/Volumes/Disk2/results/BaseCaseUKOfficeAll"
locationToProcessPDF = "~/Dropbox/Apps/Texpad/sensistivityanalysis/Images/OfficeUKWindowState.pdf"
locationToProcess = "/Volumes/Disk2/results/LinuxSol"


locationToProcess = "/media/jake/4TB/results/OfficeLearnWindow/LearningWin"
locationToProcess = "/Volumes/Disk2/results/HouseLearnWindowPMV"
locationToProcess = "/Volumes/Disk2/results/LinuxSol"

locationToProcessPDF = "~/Dropbox/Apps/Texpad/sensistivityanalysis/Images/OfficeUKWindowStateLearned.pdf"
locationToProcess = "/Volumes/Disk2/Dropbox/HPC/results/Office/learned"


locationToProcess = "/Volumes/Disk2/results/Second/BaseCaseUKOfficeAll"
locationToProcessDet = "/Volumes/Disk2/results/Second/BaseCaseUKOfficeDeterministic"
locationToProcessPDF = "~/Desktop/BaseCaseUKOfficeAllMonthlyWindow.pdf"

locationToProcess = "/Volumes/Disk2/results/Second/BaseCaseGENOfficeAll"
locationToProcessDet = "/Volumes/Disk2/results/Second/BaseCaseGENOfficeDeterministic"
locationToProcessPDF = "~/Desktop/BaseCaseGENOfficeAllMonthlyWindow.pdf"


locationToProcess = "/Volumes/2tb/PhD/results-16-04-13/results/BaseCaseUKOfficeAll"
locationToProcessDet = "/Volumes/2tb/PhD/results-16-04-13/results/BaseCaseUKOfficeDeterministic"
locationToProcessPDF = "~/Desktop/BaseCaseUKOfficeAllMonthly.pdf"
locationToProcess = "/Volumes/2tb/PhD/results-16-04-13/results/BaseCaseGENOfficeAll"
locationToProcessDet = "/Volumes/2tb/PhD/results-16-04-13/results/BaseCaseGENOfficeDeterministic"
locationToProcessPDF = "~/Desktop/BaseCaseGENOfficeAllMonthly.pdf"


dateT = function(x) {
  return((as.integer(strftime(strptime(x,"%m/%d %H:%M:%S"), format="%m"))))
}

setwd(locationToProcess)

timeStep = list.files(pattern="timestep.*[.]csv")
l = length(timeStep)
ll = l-5
#timeStep = timeStep[ll:l]
#timeStep = timeStep[1:3]


run <- function(fileName){
  x = read.csv(fileName, sep=",", header=TRUE)
  x$month = unlist(lapply(x$Date.Time,dateT))
  val <- ddply(x, .(month), summarize,
    sum = mean(BLOCK1.ZONE1_WALL_5_0_0_0_0_0_WIN.AFN.Surface.Venting.Window.or.Door.Opening.Factor....TimeStep.))
  return(val)
}
monthlyWindowState = mclapply(timeStep,run, mc.cores=3)
df <- ldply(monthlyWindowState, data.frame)


pdf(locationToProcessPDF)

boxplot(
  sum ~ month,data = df, main = "",
  xlab="", ylab="", outline=FALSE, ylim=c(0,0.3)
)
mtext(expression('Proportion Of Time Open'), side=2, line=1.9, cex=2)
mtext(expression('Month'), side=1, line=3, cex=2)

dev.off()
