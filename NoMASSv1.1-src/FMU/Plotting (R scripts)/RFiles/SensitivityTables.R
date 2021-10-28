
locationToProcess = "/Volumes/Disk2/results"
setwd(locationToProcess)
res <- readLines("R.ini")

args <- commandArgs(trailingOnly = TRUE)

print(args)

convertJulesToWMS <- function(value, size)
  (value * 0.0000002778) / size

heatingdemands <- function(x){

  print(locationToProcess)
  print(x)
  setwd(file.path(locationToProcess, x))
  RunPeriodFiles = list.files(pattern = "runperiod.*[.]csv.*")

  RunPeriod = lapply(RunPeriodFiles, read.csv)
  heatingDemand <- data.frame()
  for (i in 1:length(RunPeriod)) {
    heatingDemand = rbind(heatingDemand, returnHeatingDemandFor(RunPeriod,i))
  }
  heatingDemand = lapply(heatingDemand, convertJulesToWMS,  size = officeSize)
  heatingDemand = heatingDemand[[1]]
}

coolingdemands <- function(x){

  print(locationToProcess)
  print(x)
  setwd(file.path(locationToProcess, x))
  RunPeriodFiles = list.files(pattern = "runperiod.*[.]csv.*")

  RunPeriod = lapply(RunPeriodFiles, read.csv)
  heatingDemand <- data.frame()
  for (i in 1:length(RunPeriod)) {
    heatingDemand = rbind(heatingDemand, returnCoolingDemandFor(RunPeriod,i))
  }
  heatingDemand = lapply(heatingDemand, convertJulesToWMS,  size = officeSize)
  heatingDemand = heatingDemand[[1]]
}

testSensistivity = function(y,x){
  obj<-try(t.test(x,y, paired=TRUE), silent=TRUE)
  if (class(obj) == "try-error") {
    return(NA)
  } else {
    return(obj)
  }
}

p <- function(t){
  if(is.na(t$p.value)) {
    text <- 'NA'
  }else if(t$p.value <= 2.2e-16) {
    text <- '\\textless 2.2e-16'
  }else{
    text <- signif(t$p.value,3)
  }
  return(text)
}

writeTable = function(t, type){


  if(is.na(t)){
    cat(c(building, country, type, " ", "NA", "NA", "NA"), file=loc, sep=" & ", append=TRUE)
  }else{
    cat(c(building, country, type, " ", signif(t$statistic,3), t$parameter, p(t)), file=loc, sep=" & ", append=TRUE)
  }
  cat("  \\\\ \\hline \n", file=loc, append=TRUE)
}

building = "House"
returnHeatingDemandFor = function(data, i){
  rowSums(data[[i]][2:9])
}
returnCoolingDemandFor = function(data, i){
  rowSums(data[[i]][11:18])
}
officeSize = 67.17

if(length(grep("Office",res[1]))>0){

  building = "Office"
  officeSize = 11.41

  returnHeatingDemandFor = function(data, i) {
    data[[i]][[2]]
  }
  returnCoolingDemandFor = function(data, i) {
    data[[i]][[3]]
  }
}
country = "Geneva"
if(length(grep("UK",res[1]))>0) country = "Nottingham"
print(res)

hot = lapply(res, heatingdemands)
cold = lapply(res, coolingdemands)

loc = file.path(locationToProcess, paste0(res[1],".txt"))
print("t-test")
th <- lapply(hot[2:length(hot)], testSensistivity, x=hot[[1]])
tc <- lapply(cold[2:length(cold)], testSensistivity, x=cold[[1]])
print("Results")
cat(c("Case", "Location", "Tested Value", "Simulation", "t", "df", "p-value"), file=loc, sep=" & ", append=FALSE)
cat("  \\\\ \\hline \n", file=loc, append=TRUE)
lapply(th, writeTable, type="Heating")
lapply(tc, writeTable, type="Cooling")


t.test(hot[[1]],hot[[2]], paired=TRUE)
median(hot[[1]])
median(hot[[2]])
median(cold[[2]])
