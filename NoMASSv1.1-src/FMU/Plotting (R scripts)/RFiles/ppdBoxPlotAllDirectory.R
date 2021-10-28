library(parallel)

convertJulesToWMS <- function(value, size)
  (value * 0.0000002778) / size

dat <-function(RunPeriod) {
  x = read.csv(RunPeriod, sep=",", header=TRUE)
  heat <- x$Agent_pmv_1
  heat <- heat[!is.na(heat)]
  #heat <- mean(heat, na.rm = TRUE)
  return(heat)
}

run <- function(folder,locationToProcess) {
  print(folder)
  setwd(file.path(locationToProcess, folder))
  RunPeriodFiles = list.files(pattern = "agent.*[.]csv.*")
  #RunPeriodFiles <- RunPeriodFiles[1:20]
  heatingDemand <- NA
  heatingDemand <- mclapply(RunPeriodFiles, FUN=dat, mc.cores=3)
  m = mclapply(heatingDemand, FUN=median, mc.cores=3)
  m = unlist(m)
  heatingDemand <- unlist(heatingDemand)
  print(median(heatingDemand))
  h = hist(heatingDemand, plot = FALSE, breaks=c(-5.5:5.5))
  h$density = h$counts/sum(h$counts)*100
  labs <- paste(round(h$density), "%", sep="")
  file = paste0("~/Dropbox/Apps/Texpad/Includes/Images/DensityPMVHouse", folder)
  file = paste0(file, ".pdf")
  pdf(file)
  plot(h,freq=FALSE, xlim=c(-3,3),
       main="", ylim=c(0,80), labels = labs,
       ylab="Percent of time",
       xlab="PMV"
       )
  dev.off()
  return(m)
}

do <- function(locationToProcess){
  file = paste0("/media/jake/4TB/results/", locationToProcess)
  file = paste0("/Volumes/2tb/results/", locationToProcess)
  setwd(file)
  folders = list.files(pattern = "*")
  demands <- lapply(folders, FUN=run, locationToProcess=file)
  print(demands)
  #  folders <- c(folders,"All")
  file = paste0("~/Dropbox/Apps/Texpad/Includes/Images/boxplotcombinedPMV", locationToProcess)
  file = paste0(file, ".pdf")
  pdf(file)
  boxplot(
    demands, main = "",
    ylab = "PMV", #xlab = "Profile",
    outline = FALSE, ylim=c(-1,1),
    names = folders
  )
  dev.off()
  medianHeatingDemands <- lapply(demands, FUN=median)
  return(medianHeatingDemands)
}
building = "Office"
officeSize = 11.41

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
locations = c('HouseLearn')
locations = c('HouseLearnWindowH')

locations = c('OfficeLearn')
medianHeatingDemands <- lapply(locations, FUN=do)

medianHeatingDemands = unlist(medianHeatingDemands)
medianHeatingDemands
min(medianHeatingDemands)
max(medianHeatingDemands)

max(medianHeatingDemands) - min(medianHeatingDemands)
