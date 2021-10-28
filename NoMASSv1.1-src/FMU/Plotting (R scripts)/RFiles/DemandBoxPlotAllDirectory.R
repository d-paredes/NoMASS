

convertJulesToWMS <- function(value, size)
  (value * 0.0000002778) / size

dat <-function(RunPeriod) {
  heat <- returnHeatingDemandFor(RunPeriod)
  #heat <- returnCoolingDemandFor(RunPeriod)
  heat <- convertJulesToWMS(heat,officeSize)
  print(heat)
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
  file = paste0("/Volumes/Disk2/Dropbox/HPC/results/", locationToProcess)
  file = paste0("/Users/jake/data/PhD/results-16-06-02/", locationToProcess)
  file = paste0("/Volumes/2tb/PhD/results-16-05-02/", locationToProcess)
  print(file)
  
  setwd(file)
  folders = list.files(pattern = "BaseCaseGENOfficeAll")
  folders = sort(list.files(pattern = "*"))
  print(folders)
  
  demands <- lapply(folders, FUN=run, locationToProcess=file)
  #  folders <- c(folders,"All")
  file = paste0("~/Desktop/boxplotcombined", locationToProcess)
  file = paste0(file, ".pdf")
  s <- demands
  s <- sort(unlist(s))
  print("90: ")
  print(s[90])
  print("10: ")
  print(s[10])
  pdf(file)
  boxplot(
    demands, main = "",
    ylab = "", #xlab = "Profile",
    outline = FALSE, ylim=c(110,145),
    names = folders
  )
  mtext(expression('Heating demand (kWh/m'^2*'y)'), side=2, line=1.9, cex=1)
  mtext(expression('Length Of Timestep (Minutes)'), side=1, line=3, cex=1)
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
locations = c('OfficeRules100')
locations = c('OfficeLearnWindowHPC')

locations = c('OfficeLearn')
locations = c('GENOffice')
locations = c('Time')


medianHeatingDemands <- lapply(locations, FUN=do)

medianHeatingDemands = unlist(medianHeatingDemands)
medianHeatingDemands
min(medianHeatingDemands)
max(medianHeatingDemands)

max(medianHeatingDemands) - min(medianHeatingDemands)
