
convertJulesToWMS <- function(value, size)
  (value * 0.0000002778) / size

run <- function(folder,locationToProcess) {
  print(folder)
  setwd(file.path(locationToProcess, folder))
  RunPeriodFiles = list.files(pattern = "runperiod.*")

  RunPeriod = lapply(RunPeriodFiles, read.csv)
  heatingDemand <- data.frame()

  for (i in 1:length(RunPeriod)) {
    heat <- returnHeatingDemandFor(RunPeriod,i)
    #heat <- returnCoolingDemandFor(RunPeriod,i)

    conv <- convertJulesToWMS(heat, size = officeSize)
    heatingDemand = rbind(heatingDemand, heat)
  }
  heatingDemandx = lapply(heatingDemand, convertJulesToWMS,  size = officeSize)

  heatingDemandy <<- c(heatingDemandy,heatingDemandx[[1]])

  file = paste0("~/Dropbox/Apps/Texpad/Includes/Images/boxplotHouse", folder)
  file = paste0(file, ".pdf")
  #pdf(file)
  boxplot(heatingDemandx, main="", ylim=c(30,500))
  #dev.off()
  heatingDemandMedian = median(heatingDemand[[1]])
  watts = convertJulesToWMS(heatingDemandMedian,size = officeSize)
  print(watts)
  medianHeatingDemands <<- rbind(medianHeatingDemands,watts)
  return(heatingDemandx[[1]])
}

medianHeatingDemands <- data.frame()
heatingDemandy <- c()
do <- function(locationToProcess){
  file = paste0("/Volumes/Disk2/results/", locationToProcess)
  file = paste0("/Volumes/2tb/results/", locationToProcess)
  file = paste0("/Users/jake/data/PhD/results-16-06-02/", locationToProcess)
  file = paste0("/Users/jake/data/", locationToProcess)
  setwd(file)
  folders = list.files(pattern = "*")
  folders = list.files(pattern = "*House*")
  medianHeatingDemands <<- data.frame()
  heatingDemandy <<- c()
  demands <- lapply(folders, FUN=run, locationToProcess=file)
  #demands <- c(demands, list(heatingDemandy))
  #folders <- c(folders,"All")
  file = paste0("~/Dropbox/Apps/Texpad/Includes/Images/boxplotcombined", locationToProcess)
  file = paste0(file, ".pdf")
  #pdf(file)
  boxplot(
    demands, main = "",
    ylab = "Heating demand (kWh/m2.y)", #xlab = "Goal Set",
    outline = FALSE, #ylim=c(45,70),
    names = folders#,las=2
  )
  #dev.off()
}

returnHeatingDemandFor = function(data, i){
  rowSums(data[[i]][2:9])
}
returnCoolingDemandFor = function(data, i){
  rowSums(data[[i]][11:18])
}

officeSize = 67.17
par(mar=c(5,5,1,2)+0.1)

locations = c('HouseAllModels',
              'HouseAllModels1',
              'HouseAllModels3',
              'HouseAllModels4'
              )

locations = c('HouseSocial')
locations = c('HouseAllModels4')
locations = c('HouseRulesBox')

locations = c('HouseAllModels1')
locations = c('HouseAllModels',
              'HouseAllModels1',
              'HouseAllModels3',
              'HouseAllModels4')


locations = c('HouseVS2')
locations = c('HouseVS2')
locations = c('WindowProfilesHouse')

locations = c('HouseVS2')
locations = c('HouseLearn')

locations = c('HouseAllModels4')
locations = c('HouseAllModels')
locations = c('HouseRules')
locations = c('results')


lapply(locations, FUN=do)


median(medianHeatingDemands[[1]])



medianHeatingDemands
min(medianHeatingDemands)
max(medianHeatingDemands)

max(medianHeatingDemands) - min(medianHeatingDemands)
