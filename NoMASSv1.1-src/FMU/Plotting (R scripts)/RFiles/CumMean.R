
suppressPackageStartupMessages(library(plyr))

suppressPackageStartupMessages(library(data.table))

# Change working directory


locationToProcess = "/Volumes/Disk2/results/CUM/BaseCaseGENOfficeAll"
locationToProcessPDF = "~/Dropbox/Apps/Texpad/sensistivityanalysis/Images/OfficeGENMeanConvergence.pdf"

locationToProcess = "/Volumes/Disk2/results/Linux/"


locationToProcess = "/Volumes/Disk2/results/CUM/BaseCaseGENOfficeAll"
locationToProcessPDF = "~/Dropbox/Apps/Texpad/sensistivityanalysis/Images/OfficeGENMeanConvergence.pdf"

locationToProcess = "/Volumes/Disk2/results/CUM/BaseCaseGENHouseAll"
locationToProcessPDF = "~/Dropbox/Apps/Texpad/sensistivityanalysis/Images/HouseGENMeanConvergence.pdf"

locationToProcess = "/media/jake/4TB/results/OfficeAllModels4/Social1000"
locationToProcess = "/media/jake/4TB/results/OfficeAllModels4/Social1111"
locationToProcess = "/media/jake/4TB/results/OfficeAllModels4/Social1444"

locationToProcess = "/media/jake/4TB/results/OfficeLearn/Learning"
locationToProcessPDF = "~/Dropbox/Apps/Texpad/Includes/Images/OfficeLearningConvergence.pdf"

locationToProcess = "/media/jake/4TB/results/OfficeLearn/Learning"
locationToProcessPDF = "~/Dropbox/Apps/Texpad/Includes/Images/OfficeLearningConvergence.pdf"

locationToProcess = "/media/jake/4TB/results/OfficeLearnWindow/LearningWin"

locationToProcess = "/media/jake/4TB/results/HouseLearning"
locationToProcessPDF = "~/Dropbox/Apps/Texpad/Includes/Images/HouseLearningConvergence.pdf"


locationToProcess = "/media/jake/4TB/results/OfficeLearnWindow/LearningWin"
locationToProcessPDF = "~/Dropbox/Apps/Texpad/Includes/Images/OfficeLearningWindowConvergence.pdf"


locationToProcess = "/Volumes/Disk2/results/HouseLearnWindowPMV"
locationToProcess = "/Volumes/Disk2/results/LinuxSol"
locationToProcess = "/Volumes/2tb/results/OfficeAllModels/Democratic"
locationToProcess = "/Volumes/2tb/results-16-04-13/results/Cum/BaseCaseGENHouseAll"

locationToProcess = "/Volumes/2tb/results-16-06-02/OfficeLearning"

locationToProcess = "/Volumes/2tb/PhD/results-16-04-13/results/Cum/BaseCaseGENOfficeAll"
locationToProcessPDF = "~/Desktop/OfficeLearningWindowConvergence.pdf"


locationToProcess = "/Volumes/2tb/PhD/results-16-04-13/results/Cum/BaseCaseGENHouseAll"
locationToProcessPDF = "~/Desktop/HouseLearningWindowConvergence.pdf"

setwd(locationToProcess)

convertJulesToWMS <- function(value, size)
  (value * 0.0000002778) / size

cumulativeMeanWithError = function(x) {
  n = length(x)
  y = numeric(n)
  z = c(1:n)
  y = cumsum(x)
  y = y / z

  l = numeric(n)
  r = numeric(n)

  for (i in 1:n) {
    xx <- splitAt(x, i)
    s <- sd(xx)
    error <- qnorm(0.975) * s / sqrt(i)
    l[i] <- y[i] - error
    r[i] <- y[i] + error
  }

  df = data.frame(y, l, r)

  return(df)
}
splitAt <- function(x, pos) {
  xx <- unname(split(x, cumsum(seq_along(x) %in% pos)))
  return(as.numeric(unlist(xx)))
}

returnHeatingDemandFor = function(data, i){
  rowSums(data[[i]][2:9])
}
returnCoolingDemandFor = function(data, i){
  rowSums(data[[i]][11:18])
}
officeSize = 67.17
if(length(grep("Office",locationToProcess))>0){
  officeSize = 11.41

  returnHeatingDemandFor = function(data, i) {
    data[[i]][[2]]
  }
  returnCoolingDemandFor = function(data, i) {
    data[[i]][[3]]
  }
}

if(length(grep("Linux",locationToProcess))>0){
  officeSize = 11.41

  returnHeatingDemandFor = function(data, i) {
    data[[i]][[2]]
  }
  returnCoolingDemandFor = function(data, i) {
    data[[i]][[3]]
  }
}



RunPeriodFiles = list.files(pattern = "runperiod.*[.]csv")

RunPeriod = lapply(RunPeriodFiles, read.csv)

heatingDemand <- data.frame()
for (i in 1:length(RunPeriod)) {
  heatingDemand = rbind(heatingDemand, returnHeatingDemandFor(RunPeriod,i))
}

heatingDemand = lapply(heatingDemand, convertJulesToWMS,  size = officeSize)
heatingDemand = heatingDemand[[1]]


n = length(heatingDemand)
x = seq(1,n,1) # number of simulations
y = cumulativeMeanWithError(heatingDemand) # running mean heating demand

ma <- signif(max(y$r),3) # maximum value
mi <- signif(min(y$l),3) # minimum value


par(mar=c(5,5,1,2)+0.1)
pdf(locationToProcessPDF)
plot(
  x, y$y, type='l', xlab="",
  ylab=expression(''), ylim=c(mi,ma))
mtext(expression('Heating demand (kWh/m'^2*'y)'), side=2, line=1.9, cex=1.9)
mtext(expression('Number Of Simulations'), side=1, line=3, cex=2)
# add the error bars
lines(x, y$r, col = "blue", lty = 2)
lines(x, y$l, col = "blue", lty = 2)

legend('bottomright', legend=c("Demand", "95% Confidence Interval") , 
       lty=1:2, col=c('black', 'blue'), bty='n', cex=2)

dev.off()
if(FALSE){
y$y
heatingDemand
median(heatingDemand)


fun <- function(i){
  x1 = 1+i
  x2 = 101+i
  print(i)
  print(t.test(heatingDemand[1:x1],heatingDemand[101:x2], paired=TRUE)$p.value)
  return(t.test(heatingDemand[1:x1],heatingDemand[101:x2], paired=TRUE)$p.value)
}

y = c(1:100)
ps = unlist(lapply(y,fun))
plot(ps,type="l")#,ylim=c(0.0,0.1))



}

