

convertJulesToWMS <- function(value, size)
  (value * 0.0000002778) / size

dat <-function(RunPeriod) {
  print("      dat procedure...")
  heat <- returnHeatingDemandFor(RunPeriod)
  #heat <- returnCoolingDemandFor(RunPeriod)
  heat <- convertJulesToWMS(heat,officeSize)
  print(heat)
  return(heat)
  #return(NULL)
}

run <- function(folder,locationToProcess) {
  if(!startsWith(folder, "simulationresults"))
  {
    return(NULL)
  }
  
  print("  run procedure...")
  print(paste0("    - folder<", folder, ">"))
  print(paste0("    - locationToProcess<", locationToProcess, ">"))
  #print(folder)
  setwd(file.path(locationToProcess, folder))
  RunPeriodFiles = list.files(pattern = "runperiod.*[.]csv.*")
  print(paste0("    - RunPeriodFiles<", RunPeriodFiles, ">"))
  RunPeriod = lapply(RunPeriodFiles, read.csv)
  heatingDemand <- lapply(RunPeriod, FUN=dat)
  heatingDemand <- unlist(heatingDemand)
  print(paste0("    - median(heatingDemand)<", median(heatingDemand)))
  return(heatingDemand)
}

do <- function(locationToProcess){
  print("do procedure...")
  print(paste0("  - locationToProcess:<", locationToProcess, ">"))
  # #print(paste0("locationToProcess >> ", locationToProcess))
  # #file = paste0("/Volumes/Disk2/Dropbox/HPC/results/", locationToProcess)
  # #file = paste0("/Users/jake/data/PhD/results-16-06-02/", locationToProcess)
  # #file = paste0("/Volumes/2tb/PhD/results-16-05-02/", locationToProcess)
  # #file = paste0("/home/daps/Documents/daps_Ubuntu/GitRep/Ubuntu14-master-NoMASSv2.git/Configuration/OK/Plots/", locationToProcess)
  file = paste0("/home/daps/Documents/daps_Ubuntu/GitRep/Ubuntu14-master-NoMASSv2.git/FMU/build/ResultsLearnt/", locationToProcess)
  print(paste0("  - file<", file, ">"))
   
  setwd(file)
  folders = list.files(pattern = "SimulationConfig")
  folders = sort(list.files(pattern = "*"))
  print(paste0("  - folders<", folders, ">"))
  
  demands <- lapply(folders, FUN=run, locationToProcess=file)
  print(paste0("demands", demands))
  #  folders <- c(folders,"All")
  file = paste0("/home/daps/Documents/daps_Ubuntu/GitRep/Ubuntu14-master-NoMASSv2.git/FMU/build/ResultsLearnt/OfficeAllModels/", locationToProcess)
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
  print("        HeatingDemandFor ")
  data[[2]]
}

returnCoolingDemandFor = function(data) {
  print("        CoolingDemandFor ")
  data[[3]]
}

par(mar=c(5,5,1,2)+0.1)

# locations = c('OfficeAllModels1')
# locations = c('OfficeAllModels',
#               'OfficeAllModels1',
#               'OfficeAllModels3',
#               'OfficeAllModels4')
# 
# locations = c('OfficeAllModels',
#               'OfficeAllModels1',
#               'OfficeAllModels3',
#               'OfficeAllModels4')
# 
# locations = c('OfficeAllModels4')
# locations = c('OfficeVS2')
# locations = c('WindowProfiles')
# locations = c('OfficeSocialNotts/profiles')
# locations = c('OfficeSocialNotts/OfficeAllModels',
#               'OfficeSocialNotts/OfficeAllModels1',
#               'OfficeSocialNotts/OfficeAllModels3',
#               'OfficeSocialNotts/OfficeAllModels4')
# locations = c('OfficeSocialNotts/vs')
# locations = c('WindowProfiles')
# locations = c('Office')
# locations = c('OfficeRules100')
# locations = c('OfficeLearnWindowHPC')
# 
# locations = c('OfficeLearn')
# locations = c('GENOffice')
# locations = c('Time')
# locations = c('OfficeAllModels')
locations = c('OfficeAllModels')


# main program
print("### Main program ###")
medianHeatingDemands <- lapply(locations, FUN=do)

#9.3medianHeatingDemands = unlist(medianHeatingDemands)
#9.3medianHeatingDemands
#9.3min(medianHeatingDemands)
#9.3max(medianHeatingDemands)

#9.3max(medianHeatingDemands) - min(medianHeatingDemands)
