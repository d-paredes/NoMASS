
suppressPackageStartupMessages(library(data.table))


locationToProcess = "/Volumes/2tb/results-16-03-03/UKHouse/BaseCaseUKHouseALL"
setwd(locationToProcess)
timeStep = list.files(pattern = "timestep.*[.]csv")
ventingInteractions <- data.frame()
i=1
