

suppressPackageStartupMessages(library(plyr))
suppressPackageStartupMessages(library(data.table))

prof <- function(x){
  as.integer(which.max(unlist(x[1:20])))
}

dateT = function(x) {
  return((as.integer(strftime(strptime(x,"%m/%d %H:%M:%S"), format="%H"))))
}

run <- function(file, roomNum, locationName, detProfile){
  rlearning1 <- read.csv(file, header=FALSE)
  sapply(c(1:12), graphProf, 
         data=rlearning1, 
         room=roomNum, 
         locationName = locationName,
         detProfile = detProfile)
}

graphProf <- function(i, data, room, locationName, detProfile){
  outFolder = "~/Dropbox/Apps/Texpad/Includes/Images/"
  file <- paste0(outFolder, "LearningMonth")
  file <- paste0(file, locationName)
  file <- paste0(file, room)
  file <- paste0(file, i)
  file <- paste0(file, ".pdf")
   pdf(file)
  rlearning24 <- data[(1+(i-1)*24):(i*24),]
  p <- apply(rlearning24, 1, FUN=prof)+9
  plot(unlist(p), type="l", ylim=c(0,30),
       xlab="hour", ylab="Setpoint (c)")
  lines(detProfile, pch=22, lty=2)
   dev.off()
}

locationToProcess = "/Volumes/Disk2/Dropbox/HPC/HPCFiles/Configuration/OfficeLearnH2/Files"
setwd(locationToProcess)
weekfiles <- list.files(pattern = "Weekday-1-1-.*[.]dat")
det <- c(10,10,10,10,10,21,21,21,21,21,21,21,21,21,21,21,21,21,10,10,10,10,10,10)
run(weekfiles[1],1,"Office", det)

locationToProcess = "/Volumes/2tb/results/HouseLearning"
setwd(locationToProcess)
weekfiles <- list.files(pattern = "Weekday-1-1-.*[.]dat")
det <- c(12,12,12,12,12,18,18,18,18,18,12,12,12,12,12,12,18,18,18,18,18,18,18,12)
run(weekfiles[25],1,"House", det)
det <- c(12,12,12,12,12,12,12,12,12,12,12,12,12,12,21,21,21,21,21,21,21,21,21,12)
weekfiles <- list.files(pattern = "Weekday-2-0-.*[.]dat")
det <- c(12,12,12,12,12,18,18,18,18,18,12,12,12,12,12,12,18,18,18,18,18,18,18,12)
run(weekfiles[25],2,"House", det)
weekfiles <- list.files(pattern = "Weekday-3-0-.*[.]dat")
run(weekfiles[25],3,"House", det)
det <- c(18,18,18,18,18,18,18,18,18,12,12,12,12,12,12,12,12,12,12,12,18,18,18,18)
weekfiles <- list.files(pattern = "Weekday-4-0-.*[.]dat")
run(weekfiles[25],4,"House", det)
det <- c(10,10,10,10,10,22,22,22,22,22,22,22,22,22,22,22,22,22,10,10,10,10,10,10)
weekfiles <- list.files(pattern = "Weekday-5-0-.*[.]dat")
run(weekfiles[25],5,"House", det)

