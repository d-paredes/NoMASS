suppressPackageStartupMessages(library(data.table))
suppressPackageStartupMessages(library(plyr))

locationToProcess = "/Volumes/Disk2/results"
folder = "BaseCaseGENHouseDeterministic"

setwd(file.path(locationToProcess, folder))
ALL = list.files(pattern = "step.*[.]csv")
len <- length(ALL)
temp <- data.frame(KITCHEN=double(len),HALL=double(len),LIVINGROOM=double(len),BEDROOM=double(len),BATHROOM=double(len),LANDING=double(len),MASTERBEDROOM=double(len),OFFICE=double(len))

for (i in 1:len) {
  print(ALL[[i]])
  x = fread(ALL[[i]],sep = ",",header = TRUE,data.table=FALSE)
  temp$KITCHEN[i] = sum(x$`BLOCK1:KITCHEN:Zone Mean Air Temperature [C](TimeStep)` >= 25)
  temp$HALL[i] = sum(x$`BLOCK1:HALL:Zone Mean Air Temperature [C](TimeStep)` >= 25)
  temp$LIVINGROOM[i] = sum(x$`BLOCK1:LIVINGROOM:Zone Mean Air Temperature [C](TimeStep)` >= 25)
  temp$BEDROOM[i] = sum(x$`BLOCK2:BEDROOM:Zone Mean Air Temperature [C](TimeStep)` >= 25)
  temp$BATHROOM[i] = sum(x$`BLOCK2:BATHROOM:Zone Mean Air Temperature [C](TimeStep)` >= 25)
  temp$LANDING[i] = sum(x$`BLOCK2:LANDING:Zone Mean Air Temperature [C](TimeStep)` >= 25)
  temp$MASTERBEDROOM[i] = sum(x$`BLOCK2:MASTERBEDROOM:Zone Mean Air Temperature [C](TimeStep)` >= 25)
  temp$OFFICE[i] = sum(x$`BLOCK2:OFFICE:Zone Mean Air Temperature [C](TimeStep)` >= 25)
}

sums <- rowSums(temp)
suma <- lapply(sums,FUN=function(x) x)
sum <- median(unlist(suma))
(sum * 5) / 60
(sum * 5) / 60 /8

100 / 8760 * ((sum * 5) / 60)
100 / 8760 * ((sum * 5) / 60 /8)
