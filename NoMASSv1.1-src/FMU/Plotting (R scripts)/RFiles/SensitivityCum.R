
locationToProcess = "/media/jake/4TB/results/HouseLearn"
locationToProcess = "/media/jake/4TB/results/Office"
locationToProcess = "/Volumes/2tb/results/OfficeAllModels/"



setwd(locationToProcess)


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

building = "Office"
officeSize = 11.41

returnHeatingDemandFor = function(data, i) {
  data[[i]][[2]]
}
returnCoolingDemandFor = function(data, i) {
  data[[i]][[3]]
}

res = list.files(pattern = "*")
country = "Geneva"
if(length(grep("UK",res[1]))>0) country = "Nottingham"
print(res)

hot = lapply(res, heatingdemands)
cold = lapply(res, coolingdemands)

loc = file.path(locationToProcess, paste0(res[1],".txt"))
print("t-test")

runhot <- function(x){
  t <- testSensistivity(hot[[x]],hot[[x-1]])
  tt <- p(t)
  print(x)
  print(tt)
  
  return(tt)
}

runCold <- function(x){
  t <- testSensistivity(cold[[x]],cold[[x-1]])
  tt <- p(t)
  print(x)
  print(tt)
  print(cold[[x]])
  return(tt)
}

i = c(3:29)
th <- lapply(i,runhot)




th <- lapply(hot[2:length(hot)], testSensistivity, x=hot[[1]])

tc <- lapply(cold[2:length(cold)], testSensistivity, x=cold[[1]])


