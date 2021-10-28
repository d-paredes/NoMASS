

convertJulesToWMS <- function(value, size)
  (value * 0.0000002778) / size

dat <-function(RunPeriod) {
  heat <- returnHeatingDemandFor(RunPeriod)
  heat <- convertJulesToWMS(heat,officeSize)
  return(heat)
}

run <- function(folder,locationToProcess) {
  print(folder)
  setwd(file.path(locationToProcess, folder))
  RunPeriodFiles = list.files(pattern = "runperiod.*[.]csv.*")
  RunPeriod = lapply(RunPeriodFiles, read.csv)
  heatingDemand <- lapply(RunPeriod, FUN=dat)
  heatingDemand <- unlist(heatingDemand)
  print(median(heatingDemand))
  return(heatingDemand)
}

do <- function(locationToProcess){
  file = paste0("/media/jake/4TB/results/", locationToProcess)
  setwd(file)
  folders = list.files(pattern = "*")
  demands <- lapply(folders, FUN=run, locationToProcess=file)
  #  folders <- c(folders,"All")
  file = paste0("~/Dropbox/Apps/Texpad/Includes/Images/boxplotcombined", locationToProcess)
  file = paste0(file, ".pdf")
  pdf(file)
  boxplot(
    demands, main = "",
    ylab = "Heating demand (kWh/m2.y)", #xlab = "Profile",
    outline = FALSE, #ylim=c(70,95),
    names = folders
  )
  dev.off()
  medianHeatingDemands <- lapply(demands, FUN=median)
  return(medianHeatingDemands)
}
building = "Office"
officeSize = 11.41

returnHeatingDemandFor = function(data) {
  data[[2]]
}
returnCoolingDemandFor = function(data) {
  data[[3]]
}

par(mar=c(5,5,1,2)+0.1)

locations = c('OfficeAllModels1')
locations = c('OfficeAllModels',
              'OfficeAllModels1',
              'OfficeAllModels3',
              'OfficeAllModels4')

locations = c('OfficeAllModels',
              'OfficeAllModels1',
              'OfficeAllModels3',
              'OfficeAllModels4')

locations = c('OfficeAllModels4')
locations = c('OfficeVS2')
locations = c('WindowProfiles')
locations = c('OfficeSocialNotts/profiles')
locations = c('OfficeSocialNotts/OfficeAllModels',
              'OfficeSocialNotts/OfficeAllModels1',
              'OfficeSocialNotts/OfficeAllModels3',
              'OfficeSocialNotts/OfficeAllModels4')
locations = c('OfficeSocialNotts/vs')
locations = c('WindowProfiles')
locations = c('Office')
locations = c('OfficeLearn')
locations = c('OfficeRules100')


medianHeatingDemands <- lapply(locations, FUN=do)

medianHeatingDemands = unlist(medianHeatingDemands)
medianHeatingDemands
min(medianHeatingDemands)
max(medianHeatingDemands)

max(medianHeatingDemands) - min(medianHeatingDemands)


