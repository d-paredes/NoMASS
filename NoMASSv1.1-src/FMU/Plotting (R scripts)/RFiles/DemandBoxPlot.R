
suppressPackageStartupMessages(library(plyr))
suppressPackageStartupMessages(library("gplots"))
suppressPackageStartupMessages(library(data.table))

# Change working directory


locationToProcess = "/Volumes/Disk2/results/BaseCaseUKOfficeAll"
locationToProcess = '/Volumes/Disk2/results/OfficeSocial/Social1'
locationToProcess = '/Volumes/Disk2/results/socialLinux'
locationToProcess = '/Volumes/Disk2/results/OfficeSocial/Social1'


#par(mfrow=c(1,5))

locationToProcess = 
  '/Volumes/Disk2/Dropbox/HPC/results/OfficeTime/time/OfficeAllModelsTime5'

locationToProcess = '/home/jake/git/results/DeterOffice'
locationToProcess = '/Volumes/Disk2/Dropbox/HPC/results/HouseRules/Rule1'
locationToProcess = '/Volumes/Disk2/Dropbox/HPC/results/Office/learnWindowNo'


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

#####
##### Yearly
#####

RunPeriodFiles = list.files(pattern = "runperiod.*[.]csv")

RunPeriod = lapply(RunPeriodFiles, read.csv)


heatingDemand <- data.frame()
CoolingDemand <- data.frame()

for (i in 1:length(RunPeriod)) {
  print(RunPeriodFiles[i])
  print(convertJulesToWMS(returnHeatingDemandFor(RunPeriod,i),size = officeSize))
  heatingDemand = rbind(heatingDemand, returnHeatingDemandFor(RunPeriod,i))
  CoolingDemand = rbind(CoolingDemand, returnCoolingDemandFor(RunPeriod,i))
}

heatingDemand = lapply(heatingDemand, convertJulesToWMS,  size = officeSize)
CoolingDemand = lapply(CoolingDemand, convertJulesToWMS,  size = officeSize)
heatingDemand = heatingDemand[[1]]
CoolingDemand = CoolingDemand[[1]]
medianHeatingDemand = median(heatingDemand)
medianCoolingDemand = median(CoolingDemand)

n = length(heatingDemand)
x = seq(1,n,1) # number of simulations
y = cumulativeMeanWithError(heatingDemand) # running mean heating demand

ma <- signif(max(y$r),3) # maximum value
mi <- signif(min(y$l),3) # minimum value

notes <- data.frame("heatingDemand" = NA, "coolingDemand" = NA)
notes$heatingDemand = medianHeatingDemand
notes$coolingDemand = medianCoolingDemand

textplot(notes)

#h <- hist(
#  heatingDemand, breaks = 10, col = "red", xlab = "",
#  main = "Heating Demand"
#)

#h <- hist(
#  main = "Cooling Demand"
#  CoolingDemand, breaks = 10, col = "red", xlab = "",
#)

boxplot(
  heatingDemand, main = "",
  xlab = "", ylab = "Heating Demand(kWh/m2.y)",outline = FALSE, ylim = c(50,120)
)
officeSize

median(heatingDemand)
median(CoolingDemand)
#heatingDemand = sort(heatingDemand)
min(heatingDemand)
max(heatingDemand)

max(heatingDemand[5:95])
min(heatingDemand[5:95])
