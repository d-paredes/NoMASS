

converge <- function(file){
  rlearning1 <- read.csv(file, header=FALSE)
  
  con <- rep(0,288)
  for (i in 1:288) {
    con[i] <- which.max(rlearning1[i,])
  }
  
  set <- which(con != convergeDF)
  convergeDF <<- con
  print(length(set))
  return(length(set))
}


locationToProcess = "/Volumes/Disk2/results/Linux/"

locationToProcess = "/media/jake/4TB/results/HouseLearn/Learning"

setwd(locationToProcess)

par(mar=c(3,5,1,2)+0.1)
par(mfrow=c(1,1))

weekfiles <- list.files(pattern = "Weekday-1-0-.*[.]dat")
convergeDF <- rep(0,288)
conv <- lapply(weekfiles, FUN=converge)
plot(unlist(conv), type="l",ylim=c(0,288))

weekfiles <- list.files(pattern = "Weekday-1-1-.*[.]dat")
convergeDF <- rep(0,48)
conv <- lapply(weekfiles, FUN=converge)
plot(unlist(conv), type="l")


weekfiles <- list.files(pattern = "Weekend-1-1-.*[.]dat")
convergeDF <- rep(0,24)
conv <- lapply(weekfiles, FUN=converge)
plot(unlist(conv), type="l")


weekfiles <- list.files(pattern = "Weekend-1-0-.*[.]dat")
convergeDF <- rep(0,24)
conv <- lapply(weekfiles, FUN=converge)
plot(unlist(conv), type="l")

