

returnCoolingDemandForO = function(data, i) {
  data[[i]][[3]]
}

returnCoolingDemandForH = function(data, i){
  rowSums(data[[i]][11:18])
}


returnHeatingDemandForO = function(data, i) {
  data[[i]][[2]]
}

returnHeatingDemandForH = function(data, i){
  rowSums(data[[i]][2:9])
}

convertJulesToWMS <- function(value, size)
  (value * 0.0000002778) / size


setwd(file.path('/Volumes/2tb/PhD/results-16-03-14/UKOffice', 'BaseCaseUKOfficeAll'))
RunPeriodFiles = list.files(pattern = "runperiod.*[.]csv")
RunPeriodUKO = lapply(RunPeriodFiles, read.csv)
RunPeriodUKOD = read.csv('/Volumes/2tb/PhD/results-16-03-14/BaseCaseUKOfficeDeterministic/Allrunperiod1.csv')
heatingDemandUKO <- data.frame()
heatingDemandUKOD <- RunPeriodUKOD[[2]]

setwd(file.path('/Volumes/2tb/PhD/results-16-03-14/GENOffice', 'BaseCaseGENOfficeAll'))
RunPeriodFiles = list.files(pattern = "runperiod.*[.]csv")
RunPeriodGEO = lapply(RunPeriodFiles, read.csv)
RunPeriodGEOD = read.csv('/Volumes/2tb/PhD/results-16-03-14/BaseCaseGENOfficeDeterministic/Allrunperiod1.csv')
heatingDemandGEO <- data.frame()
heatingDemandGEOD <- RunPeriodGEOD[[2]]

setwd(file.path('/Volumes/2tb/PhD/results-16-03-14/UKHouse', 'BaseCaseUKHouseAll'))
RunPeriodFiles = list.files(pattern = "runperiod.*[.]csv")
RunPeriodUKH = lapply(RunPeriodFiles, read.csv)
RunPeriodUKHD = read.csv('/Volumes/2tb/PhD/results-16-03-14/BaseCaseUKHouseDeterministic/Allrunperiod1.csv')
heatingDemandUKH <- data.frame()
heatingDemandUKHD <- rowSums(RunPeriodUKHD[2:9])

setwd(file.path('/Volumes/2tb/PhD/results-16-03-14/GENHouse', 'BaseCaseGENHouseAll'))
RunPeriodFiles = list.files(pattern = "runperiod.*[.]csv")
RunPeriodGEH = lapply(RunPeriodFiles, read.csv)
RunPeriodGEHD = read.csv('/Volumes/2tb/PhD/results-16-03-14/BaseCaseGENHouseDeterministic/Allrunperiod1.csv')
heatingDemandGEH <- data.frame()
heatingDemandGEHD <- rowSums(RunPeriodGEHD[2:9])



for (i in 1:100) {
  heatingDemandUKO = rbind(heatingDemandUKO, returnHeatingDemandForO(RunPeriodUKO,i))
  heatingDemandGEO = rbind(heatingDemandGEO, returnHeatingDemandForO(RunPeriodGEO,i))
  heatingDemandUKH = rbind(heatingDemandUKH, returnHeatingDemandForH(RunPeriodUKH,i))
  heatingDemandGEH = rbind(heatingDemandGEH, returnHeatingDemandForH(RunPeriodGEH,i))
}

heatingDemandUKO = lapply(heatingDemandUKO, convertJulesToWMS,  size = 11.41)

heatingDemandUKOD = convertJulesToWMS(heatingDemandUKOD, size = 11.41)

heatingDemandGEO = lapply(heatingDemandGEO, convertJulesToWMS,  size = 11.41)
heatingDemandGEOD = convertJulesToWMS(heatingDemandGEOD, size = 11.41)

heatingDemandUKH = lapply(heatingDemandUKH, convertJulesToWMS,  size = 67.17)
heatingDemandUKHD = convertJulesToWMS(heatingDemandUKHD, size = 67.17)

heatingDemandGEH = lapply(heatingDemandGEH, convertJulesToWMS,  size = 67.17)
heatingDemandGEHD = convertJulesToWMS(heatingDemandGEHD, size = 67.17)






setwd(file.path('/Volumes/2tb/PhD/results-16-03-14/GENHouse', 'BaseCaseGENHouseAll'))
RunPeriodFiles = list.files(pattern = "runperiod.*[.]csv")
RunPeriodGEH = lapply(RunPeriodFiles, read.csv)
RunPeriodGEHD = read.csv('/Volumes/2tb/PhD/results-16-03-14/BaseCaseGENHouseDeterministic/Allrunperiod1.csv')
coolingDemandGEH <- data.frame()
coolingDemandGEHD <- rowSums(RunPeriodGEHD[11:18])

setwd(file.path('/Volumes/2tb/PhD/results-16-03-14/GENOffice', 'BaseCaseGENOfficeAll'))
RunPeriodFiles = list.files(pattern = "runperiod.*[.]csv")
RunPeriodGEO = lapply(RunPeriodFiles, read.csv)
RunPeriodGEOD = read.csv('/Volumes/2tb/PhD/results-16-03-14/BaseCaseGENOfficeDeterministic/Allrunperiod1.csv')
coolingDemandGEO <- data.frame()
coolingDemandGEOD <- RunPeriodGEOD[[3]]

for (i in 1:100) {
  coolingDemandGEO = rbind(coolingDemandGEO, returnCoolingDemandForO(RunPeriodGEO,i))
  coolingDemandGEH = rbind(coolingDemandGEH, returnCoolingDemandForH(RunPeriodGEH,i))
}

coolingDemandGEO = lapply(coolingDemandGEO, convertJulesToWMS,  size = 11.41)
coolingDemandGEOD = convertJulesToWMS(coolingDemandGEOD, size = 11.41)

coolingDemandGEH = lapply(coolingDemandGEH, convertJulesToWMS,  size = 67.17)
coolingDemandGEHD = convertJulesToWMS(coolingDemandGEHD, size = 67.17)

boxes <-
  data.frame(
    "a" = c(1:100),"b" = NA,"c" = NA,"d" = NA,"e" = NA,"f" = NA
  )
boxesD <-  data.frame(
  "a" = c(1:1),"b" = NA,"c" = NA,"d" = NA,"e" = NA,"f" = NA
)
boxes[1] = heatingDemandUKO[1]
boxesD[1] = heatingDemandUKOD
boxes[2] = heatingDemandGEO[1]
boxesD[2] = heatingDemandGEOD
boxes[3] = heatingDemandUKH[1]
boxesD[3] = heatingDemandUKHD
boxes[4] = heatingDemandGEH[1]
boxesD[4] = heatingDemandGEHD
boxes[5] = coolingDemandGEO[1]
boxesD[5] = coolingDemandGEOD
boxes[6] = coolingDemandGEH[1]
boxesD[6] = coolingDemandGEHD

pdf("~/Desktop/CompareHeatingDemand.pdf")
par(mar=c(5,5,1,2)+0.1)
boxplot(
  boxes, main = "",
  xlab = "", ylab = "",outline = FALSE, ylim=c(0,130),
  xaxt="n"
)

xcoord <- rep(1.0:6.0)
storage.mode(xcoord) <- "double"
par(new = T)
plot(
  xcoord, boxesD, xlim = c(0.5, 6.5),ylim = c(0,130), axes = F, ylab ="", xlab = ""
)

axis(1,at=c(1,2,3,4,5,6),adj=1, tick=F, line=1.5,labels=c("Nottingham\nOffice\nHeating", "Geneva\nOffice\nHeating", "Nottingham\nHouse\nHeating", "Geneva\nHouse\nHeating", "Geneva\nOffice\nCooling", "Geneva\nHouse\nCooling")) 

mtext(expression('Heating demand (kWh/m'^2*'y)'), side=2, line=1.9, cex=1)
dev.off()


