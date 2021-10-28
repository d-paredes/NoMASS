
convertJulesToWMS <- function(value, size)
  (value * 0.0000002778) / size


officeSize = 11.41

returnHeatingDemandFor = function(data, i) {
  data[[i]][[2]]
}
returnCoolingDemandFor = function(data, i) {
  data[[i]][[3]]
}


func <- function(folder){
  setwd(folder)
  RunPeriodFiles = list.files(pattern = "runperiod.*[.]csv")
  RunPeriod = lapply(RunPeriodFiles, read.csv)
  
  heatingDemand <- data.frame()
  
  for (i in 1:length(RunPeriod)) {
    print(RunPeriodFiles[i])
    print(convertJulesToWMS(returnHeatingDemandFor(RunPeriod,i),size = officeSize))
    heatingDemand = rbind(heatingDemand, returnHeatingDemandFor(RunPeriod,i))
    
  }
  
  heatingDemand = lapply(heatingDemand, convertJulesToWMS,  size = officeSize)
  return(heatingDemand[[1]])
}


min1 <- func('/media/jake/4TB/results/Time/OfficeAllModelsTime1')
min2 <- func('/media/jake/4TB/results/Time/OfficeAllModelsTime2')
min3 <- func('/media/jake/4TB/results/Time/OfficeAllModelsTime3')
min4 <- func('/media/jake/4TB/results/Time/OfficeAllModelsTime4')
min5 <- func('/media/jake/4TB/results/Time/OfficeAllModelsTime5')
min6 <- func('/media/jake/4TB/results/Time/OfficeAllModelsTime6')
min10 <- func('/media/jake/4TB/results/Time/OfficeAllModelsTime10')
min12 <- func('/media/jake/4TB/results/Time/OfficeAllModelsTime12')
min15 <- func('/media/jake/4TB/results/Time/OfficeAllModelsTime15')
min20 <- func('/media/jake/4TB/results/Time/OfficeAllModelsTime20')
min30 <- func('/media/jake/4TB/results/Time/OfficeAllModelsTime30')


df <- data.frame(min1,min2,min3,min4,min5,min6,min10,min12,min15,min20,min30)

par(mar=c(3,5,1,2)+0.1)
pdf('~/Dropbox/Apps/Texpad/Includes/Images/TimeStepAnalysis.pdf')
boxplot(
  df, main = "",
  xlab = "Length Of Timestep (Minutes)", ylab = "Heating Demand (kWh/m2.y)",
  outline = FALSE, ylim = c(110,145),
  names = c(1,2,3,4,5,6,10,12,15,20,30)
)
dev.off()
