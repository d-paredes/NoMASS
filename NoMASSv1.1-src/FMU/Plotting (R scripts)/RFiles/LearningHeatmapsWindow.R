

runHeat <- function(file){
  
  par(mar=c(3,5,1,2)+0.1)
  par(mfrow=c(1,1))
  
  rlearning1 <- read.csv(file, header=FALSE)
  mat <- data.matrix(rlearning1[1:20,1:2])
  my_palette <- colorRampPalette(c("red", "yellow", "green"))(n = 100)
  heatmap(mat, Rowv=NA, Colv=NA, col=my_palette, main=file)
}


locationToProcess = "/Volumes/Disk2/results/Linux/"
locationToProcess = "/home/jake/git/results/learn"

locationToProcess = "/Volumes/Disk2/results/HouseLearnWindowPMV"
locationToProcess = "/Volumes/Disk2/results/LinuxSol"

setwd(locationToProcess)

weekfiles <- list.files(pattern = "window-1-0-.*[.]dat")
lapply(weekfiles[0:50], FUN=runHeat)
