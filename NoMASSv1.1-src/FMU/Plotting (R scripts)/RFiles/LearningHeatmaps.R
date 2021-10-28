

runHeat <- function(file){
  
  par(mar=c(3,5,1,2)+0.1)
  par(mfrow=c(1,1))
  
  rlearning1 <- read.csv(file, header=FALSE)
  mat <- data.matrix(rlearning1[1:24,1:20])
  my_palette <- colorRampPalette(c("red", "yellow", "green"))(n = 100)
  heatmap(mat, Rowv=NA, Colv=NA, col=my_palette)
}


locationToProcess = "/Volumes/Disk2/results/Linux/"
locationToProcess = "/home/jake/git/results/learn"
setwd(locationToProcess)

weekfiles <- list.files(pattern = "Weekday-1-0-.*[.]dat")
lapply(weekfiles[0:50], FUN=runHeat)
