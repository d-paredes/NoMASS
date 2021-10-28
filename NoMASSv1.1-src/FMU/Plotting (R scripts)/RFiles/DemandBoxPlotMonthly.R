
suppressPackageStartupMessages(library(plyr))

suppressPackageStartupMessages(library(data.table))

# Change working directory


locationToProcess = "/Volumes/2tb/PhD/results-16-04-13/results/Second/BaseCaseUKOfficeAll"
locationToProcessDet = "/Volumes/2tb/PhD/results-16-04-13/results/Second/BaseCaseUKOfficeDeterministic"
locationToProcessPDF = "~/Desktop/BaseCaseUKOfficeAllMonthly.pdf"


locationToProcess = "/Volumes/2tb/PhD/results-16-04-13/results/BaseCaseGENOfficeAll"
locationToProcessDet = "/Volumes/2tb/PhD/results-16-04-13/results/BaseCaseGENOfficeDeterministic"
locationToProcessPDF = "~/Desktop/BaseCaseGENOfficeAllMonthly.pdf"

locationToProcess = "/Volumes/2tb/PhD/results-16-04-13/results/BaseCaseUKOfficeAll"
locationToProcessDet = "/Volumes/2tb/PhD/results-16-04-13/results/BaseCaseUKOfficeDeterministic"
locationToProcessPDF = "~/Desktop/BaseCaseUKOfficeAllMonthly.pdf"

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
##### Monthly
#####
monthly <- list.files(pattern = "monthly.*[.]csv")
monthly <- lapply(monthly, read.csv)


monthlyDF <-
  data.frame(
    "Jan" = NA,"Feb" = NA,"Mar" = NA,"Apr" = NA,"May" = NA,"Jun" = NA,"Jul" =
      NA,"Aug" = NA,"Sep" = NA,"Oct" = NA,"Nov" = NA,"Dec" = NA
  )

for (i in 1:length(monthly)) {
  monthlyDF[i,] = lapply(
    returnHeatingDemandFor(monthly,i), convertJulesToWMS,  size = officeSize
  )
}


pdf(locationToProcessPDF)
par(mar=c(5,5,1,2)+0.1)
boxplot(
  monthlyDF, main = "",
  xlab = "", ylab = "",outline = FALSE, ylim = c(0,30),
  names = c(1:12)
)
mtext(expression('Heating demand (kWh/m'^2*'y)'), side=2, line=1.9, cex=2)
mtext(expression('Month'), side=1, line=3, cex=2)


setwd(locationToProcessDet)
monthlyDet <- list.files(pattern = "monthly.*[.]csv")
monthlyDet <- lapply(monthlyDet, read.csv)

monthlyDF <-
  data.frame(
    "Jan" = NA,"Feb" = NA,"Mar" = NA,"Apr" = NA,"May" = NA,"Jun" = NA,"Jul" =
      NA,"Aug" = NA,"Sep" = NA,"Oct" = NA,"Nov" = NA,"Dec" = NA
  )

for (i in 1:length(monthlyDet)) {
  monthlyDF[i,] = lapply(
    returnHeatingDemandFor(monthlyDet,i), convertJulesToWMS,  size = officeSize
  )
}

xcoord <- rep(1.0:12.0)
storage.mode(xcoord) <- "double"
par(new = T)
plot(xcoord, monthlyDF, xlim=c(0.5, 12.5), ylim=c(0, 30), axes=F, ylab="", xlab="")

#stripchart(monthlyDF, vertical = TRUE,
#           method = "overplot", add = TRUE, pch = 16, col = 'blue')

dev.off()

