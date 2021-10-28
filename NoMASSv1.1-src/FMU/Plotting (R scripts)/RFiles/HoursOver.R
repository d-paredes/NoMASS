suppressPackageStartupMessages(library(data.table))
suppressPackageStartupMessages(library(plyr))

locationToProcess = "/Volumes/Disk2/results"
folder = "BaseCaseGENOfficeDeterministic"

setwd(file.path(locationToProcess, folder))
ALL = list.files(pattern = "step.*[.]csv")

temp <- data.frame()

for (i in 1:length(ALL)) {
  x = fread(ALL[[i]],sep = ",",header = TRUE)
  temp = rbind(temp, sum(x$`BLOCK1:ZONE1:Zone Mean Air Temperature [C](TimeStep)` >= 25))
  print(ALL[[i]])
}

tempm <- median(temp[[1]])
(tempm * 5) / 60

100 / 8760 * ((tempm * 5) / 60)
