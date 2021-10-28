
suppressPackageStartupMessages(library(plyr))
suppressPackageStartupMessages(library(data.table))

# Change working directory

locationToProcess = '/Volumes/Disk2/results/OfficeSocial/Social1'

locationToProcess = '/Volumes/Disk2/results/socialLinux'
locationToProcess = '/Volumes/Disk2/results/socialLinux1'


locationToProcess = "/Volumes/Disk2/results/BaseCaseGENOfficeAll"
locationToProcessPDF = "~/Dropbox/Apps/Texpad/sensistivityanalysis/Images/OfficeGENWindowState.pdf"

locationToProcess = "/Volumes/Disk2/results/BaseCaseUKOfficeAll"
locationToProcessPDF = "~/Dropbox/Apps/Texpad/sensistivityanalysis/Images/OfficeUKWindowState.pdf"


dateT = function(x) {
  return((as.integer(strftime(strptime(x,"%m/%d %H:%M:%S"), format="%m"))))
}

dateTH = function(x) {
  return((as.integer(strftime(strptime(x,"%m/%d %H:%M:%S"), format="%H"))))
}

setwd(locationToProcess)

timeStep = list.files(pattern="timestep.*[.]csv")
monthlyWindowState <- data.frame()

i=1
for (i in 1:length(timeStep)) {
  x = fread(timeStep[[i]], sep=",", header=TRUE)
  x$month = unlist(lapply(x$`Date/Time`,dateT))
  x$hour = unlist(lapply(x$`Date/Time`,dateTH))
  monthlyWindowState = rbind(monthlyWindowState, 
        ddply(x, .(month, hour), summarize,
        sum = sum(`BLOCK1:ZONE1_WALL_5_0_0_0_0_0_WIN:AFN Surface Venting Window or Door Opening Factor [](TimeStep)`)))
}
monthlyWindowStatex =ddply(monthlyWindowState, .(month, hour), summarize,
                                 sum = mean(`sum`))

#pdf(locationToProcessPDF)

boxplot(
  sum ~ hour,data = monthlyWindowState, main = "", 
  xlab="Month", ylab="Proportion Of Time Open", outline=FALSE, ylim=c(0,0.4)
)

mat <- daply(monthlyWindowStatex, .(month, hour), function(x) x$sum)
my_palette <- colorRampPalette(c("black", "white"))(n = 100)
heatmap(mat, Rowv=NA, Colv=NA, col=my_palette)


#dev.off()
