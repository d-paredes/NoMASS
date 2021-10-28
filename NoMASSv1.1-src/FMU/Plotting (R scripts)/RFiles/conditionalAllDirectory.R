
run <- function(folder,locationToProcess) {
  setwd(file.path(locationToProcess, folder))
  RunPeriodFiles = list.files(pattern = "timestep.*[.]csv")
  heatingDemand <- data.frame()
  for (i in 1:length(RunPeriodFiles)) {
    x = fread(RunPeriodFiles[[i]],sep = ",",header = TRUE)
    count = 0
    for (j in 2:length(x[[1]])) {
      if(x$`BLOCK1:ZONE1_WALL_5_0_0_0_0_0_WIN:AFN Surface Venting Window or Door Opening Factor [](TimeStep)`[j] != x$`BLOCK1:ZONE1_WALL_5_0_0_0_0_0_WIN:AFN Surface Venting Window or Door Opening Factor [](TimeStep)`[j-1]){
        if(x$`BLOCK1:ZONE1_WALL_5_0_0_0_0_0_WIN:Window Shading Fraction [Fraction](TimeStep)`[j] != x$`BLOCK1:ZONE1_WALL_5_0_0_0_0_0_WIN:Window Shading Fraction [Fraction](TimeStep)`[j-1]){
        count = count + 1
        }
      }
    }
    heatingDemand = rbind(heatingDemand, count)
    print(i)
  }
  return(heatingDemand[[1]])
}


do <- function(locationToProcess){
  file = paste0("/media/jake/4TB/results/", locationToProcess)
  setwd(file)
  folders = list.files(pattern = "*")
  demands <- lapply(folders, FUN=run, locationToProcess=file)
  file = paste0("~/Dropbox/Apps/Texpad/Includes/Images/boxplotCombined", locationToProcess)
  file = paste0(file, ".pdf")
  pdf(file)
  boxplot(
    demands, main = "",
    xlab = "Profile", ylab = "Combined Interactions",
    outline = FALSE, ylim=c(0,10),
    names = folders
  )
  dev.off()
}

par(mar=c(5,5,1,2)+0.1)

locations = c('OfficeAllModels1')
locations = c('OfficeVS2')

locations = c('WindowProfiles')
locations = c('OfficeAllModels',
              'OfficeAllModels1',
              'OfficeAllModels3',
              'OfficeAllModels4'
)

locations = c('OfficeAllModels4')
locations = c('OfficeVS2')
locations = c('OfficeLearn')
locations = c('OfficeCombined')
lapply(locations, FUN=do)




